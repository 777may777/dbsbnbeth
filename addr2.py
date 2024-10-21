import asyncio
import requests
import json
import time
import websockets

# Configuración de nodos RPC por red
RPC_NODOS = {
    'bnb': [
        'wss://bsc-rpc.publicnode.com',
        'https://binance.llamarpc.com',
        'https://bsc-mainnet.public.blastapi.io',
        'wss://bsc.callstaticrpc.com',
        'https://bsc-pokt.nodies.app'
    ],
    'eth': [
        'https://eth.llamarpc.com',
        'wss://mainnet.gateway.tenderly.co',
        'wss://ethereum.callstaticrpc.com',
        'wss://ethereum-rpc.publicnode.com',
        'https://rpc.ankr.com/eth'
    ]
}

# Parámetros
ARCHIVO_RESULTADO = 'result.txt'
MIN_USD_VALUE = 100  # Valor mínimo en USD para guardar direcciones
BNB_PRECIO = 215  # Precio actual de BNB en USD
ETH_PRECIO = 1650  # Precio actual de ETH en USD

# Función para conectar a WebSocket y obtener el bloque más reciente
async def obtener_numero_bloque_actual_ws(rpc_url):
    try:
        if rpc_url.startswith('wss'):
            async with websockets.connect(rpc_url) as websocket:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "eth_blockNumber",
                    "params": [],
                    "id": 1
                }
                await websocket.send(json.dumps(payload))
                response = await websocket.recv()
                result = json.loads(response)
                return int(result['result'], 16)
        else:
            response = requests.post(rpc_url, json={
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            }, timeout=10)
            result = response.json()
            return int(result['result'], 16)
    except Exception as e:
        print(f"Error al conectarse al RPC {rpc_url}: {e}")
        return None

# Función para obtener las transacciones del bloque
async def obtener_transacciones_del_bloque_ws(rpc_url, block_number):
    try:
        if rpc_url.startswith('wss'):
            async with websockets.connect(rpc_url) as websocket:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "eth_getBlockByNumber",
                    "params": [hex(block_number), True],
                    "id": 1
                }
                await websocket.send(json.dumps(payload))
                response = await websocket.recv()
                block = json.loads(response).get('result', {})
                return block.get('transactions', [])
        else:
            response = requests.post(rpc_url, json={
                "jsonrpc": "2.0",
                "method": "eth_getBlockByNumber",
                "params": [hex(block_number), True],
                "id": 1
            }, timeout=10)
            block = response.json().get('result', {})
            return block.get('transactions', [])
    except Exception as e:
        print(f"Error obteniendo transacciones del bloque en {rpc_url}: {e}")
        return []

# Filtrar direcciones por valor mínimo en USD
def filtrar_direcciones_por_valor(transacciones, min_usd_value, precio_moneda):
    direcciones = set()
    for tx in transacciones:
        eth_value = int(tx['value'], 16) / 10**18
        usd_value = eth_value * precio_moneda
        if usd_value >= min_usd_value:
            if tx['from']:
                direcciones.add(tx['from'])
            if tx['to']:
                direcciones.add(tx['to'])
    return direcciones

# Guardar direcciones en archivo
def guardar_direcciones_en_archivo(direcciones, archivo):
    with open(archivo, 'a') as f:
        for direccion in direcciones:
            f.write(direccion + '\n')

# Función principal para procesar bloques en cada red
async def procesar_bloques(nodos_rpc, red, precio_moneda, min_usd_value):
    archivo_resultado = f'{red}_result.txt'
    ultimo_bloque = await obtener_numero_bloque_actual_ws(nodos_rpc[0])

    while True:
        for nodo in nodos_rpc:
            nuevo_bloque = await obtener_numero_bloque_actual_ws(nodo)
            if nuevo_bloque and nuevo_bloque > ultimo_bloque:
                print(f"Nuevo bloque detectado en {red}: {nuevo_bloque}")
                
                transacciones = await obtener_transacciones_del_bloque_ws(nodo, nuevo_bloque)
                direcciones = filtrar_direcciones_por_valor(transacciones, min_usd_value, precio_moneda)
                
                if direcciones:
                    guardar_direcciones_en_archivo(direcciones, archivo_resultado)
                    print(f"Direcciones guardadas en {archivo_resultado}")
                
                ultimo_bloque = nuevo_bloque
            await asyncio.sleep(1)  # Pausa pequeña entre iteraciones para no sobrecargar

# Función para elegir la red y empezar la verificación
async def main():
    print("Selecciona una red:")
    print("1. BNB")
    print("2. ETH")
    
    eleccion = input("Elige una red (1/2): ")
    
    if eleccion == '1':
        red = 'bnb'
        precio_moneda = BNB_PRECIO
    elif eleccion == '2':
        red = 'eth'
        precio_moneda = ETH_PRECIO
    else:
        print("Opción inválida")
        return

    nodos_rpc = RPC_NODOS[red]
    await procesar_bloques(nodos_rpc, red, precio_moneda, MIN_USD_VALUE)

if __name__ == "__main__":
    asyncio.run(main())