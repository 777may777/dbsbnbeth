### Descripción del Script

**Español:**

Este script en Python se conecta a los nodos de las redes blockchain BNB y ETH a través de WebSocket y HTTP para obtener las transacciones en bloques recientes. El propósito del script es filtrar direcciones involucradas en transacciones con un valor mínimo equivalente a 100 USD y guardar estas direcciones en archivos separados por red (por ejemplo, `bnb_result.txt` para BNB y `eth_result.txt` para Ethereum).

El programa alterna entre múltiples nodos para evitar errores de conexión o sobrecarga en un solo servidor. El usuario puede seleccionar la red (BNB o ETH) y el script automáticamente descargará los bloques, filtrará las transacciones y guardará las direcciones.

**Inglés:**

This Python script connects to BNB and ETH blockchain nodes via WebSocket and HTTP to retrieve transactions from recent blocks. The script's purpose is to filter addresses involved in transactions with a minimum value equivalent to 100 USD and save these addresses in separate files by network (e.g., `bnb_result.txt` for BNB and `eth_result.txt` for Ethereum).

The program alternates between multiple nodes to avoid connection errors or overloading a single server. Users can select the network (BNB or ETH), and the script will automatically fetch blocks, filter transactions, and store the addresses.

---

### Nota de Descargo | Disclaimer

**Español:**

Este script está diseñado exclusivamente con fines educativos. El uso indebido de este código para actividades no autorizadas, como la minería o la manipulación de datos de blockchain, es responsabilidad exclusiva del usuario. El autor no se hace responsable de los daños directos o indirectos que resulten del uso de este software.

**Inglés:**

This script is intended solely for educational purposes. Misuse of this code for unauthorized activities, such as mining or manipulating blockchain data, is the sole responsibility of the user. The author is not liable for any direct or indirect damages resulting from the use of this software.
