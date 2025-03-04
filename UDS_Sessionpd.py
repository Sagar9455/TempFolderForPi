import logging
import udsoncan
from udsoncan.connections import IsoTPSocketConnection

# Enable debug logging to check UDS communication
logging.basicConfig(level=logging.DEBUG)

# Define CAN interface and UDS Tx/Rx IDs
interface = "can0"
tx_id = 0x18DB33F1  # Replace with your ECU's Request ID
rx_id = 0x18DAF190  # Replace with your ECU's Response ID

# Setup ISO-TP connection with padding enabled
conn = IsoTPSocketConnection(interface, rxid=rx_id, txid=tx_id, is_extended_id=True, padding_byte=0x00)

# UDS Client setup
with udsoncan.Client(conn, request_timeout=2) as client:
    try:
        response = client.change_session(udsoncan.DiagnosticSessionControl.DefaultSession)  # 0x10 0x01
        
        if response.positive:
            print("Default Session Activated Successfully!")
        else:
            print(f"Session Change Failed! Response: {response}")
    
    except Exception as e:
        print(f"Error: {e}")
