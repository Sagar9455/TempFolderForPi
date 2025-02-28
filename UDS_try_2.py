import can
import isotp
from udsoncan.client import Client
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.services import ReadDataByIdentifier

# Define Tx and Rx CAN IDs (Extended 29-bit CAN IDs)
TX_ID = 0x1A30C0B1  # ECU Address (Request)
RX_ID = 0x1A30CB10  # ECU Reply Address (Response)

# Setup CAN bus & ISO-TP
conn = IsoTPSocketConnection('can0', isotp.Address(isotp.AddressingMode.Normal_29bits, txid=TX_ID, rxid=RX_ID))

# Start UDS Client
with Client(conn, request_timeout=2) as client:
    try:
        # Read VIN (DID 0xF190)
        vin_response = client.read_data_by_identifier(0xF190)
        vin = ''.join(chr(byte) for byte in vin_response)
        print(f"VIN Number: {vin}")

    except Exception as e:
        print(f"Error: {e}")
