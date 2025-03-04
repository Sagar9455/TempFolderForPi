import logging
import udsoncan
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client
from udsoncan.services import DiagnosticSessionControl
from udsoncan.configs import default_config  # Import default config
from udsoncan import Address  # Import Address to fix the error

# Enable debug logging to check UDS communication
logging.basicConfig(level=logging.DEBUG)

# Define CAN interface
interface = "can0"

# Define UDS Tx/Rx IDs
tx_id = 0x18DB33F1  # Modify based on your ECU
rx_id = 0x18DAF190  # Modify based on your ECU

# Define the addressing mode using the Address class
uds_address = Address(
    rxid=rx_id,  # ECU response ID
    txid=tx_id,  # Tester request ID
    is_extended_id=True  # Using 29-bit CAN IDs
)

# Define UDS configuration manually
config = default_config  # Load the default configuration
config["padding_byte"] = 0xAA  # Ensure padding is set to 0xAA
config["use_server_timing"] = False  # Use client timing
config["exception_on_negative_response"] = False  # Do not raise exceptions on negative responses

# Define connection with correct Address object
conn = IsoTPSocketConnection(interface, uds_address)

# UDS Client setup with the manual config
with Client(conn, request_timeout=2, config=config) as client:
    try:
        response = client.change_session(DiagnosticSessionControl.DefaultSession)  # 0x10 0x01
        
        if response.positive:
            print("✅ Default Session Activated Successfully!")
        else:
            print(f"❌ Session Change Failed! Response: {response}")
    
    except Exception as e:
        print(f"⚠️ Error: {e}")
