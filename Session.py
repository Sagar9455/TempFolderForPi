import logging
import udsoncan
from udsoncan.connections import IsoTPSocketConnection

# Enable debug logging to check UDS communication
logging.basicConfig(level=logging.DEBUG)

# Define CAN interface and UDS Tx/Rx IDs
interface = "can0"
tx_id = 0x18DB33F1  # Modify based on your ECU
rx_id = 0x18DAF190  # Modify based on your ECU

# Define UDS configuration manually
config = {
    "use_server_timing": False,  # Use client timing
    "exception_on_negative_response": False,  # Do not raise exceptions on negative responses
    "security_algo": None,  # No security algorithm
    "security_algo_params": None,
    "standard_version": 2013,  # UDS standard version
    "padding_byte": 0x00,  # Ensure padding is enabled
}

# Define connection with padding enabled
conn = IsoTPSocketConnection(
    interface, 
    rxid=rx_id, 
    txid=tx_id, 
    is_extended_id=True, 
    padding_byte=0x00  # Enable padding
)

# UDS Client setup with the manual config
with udsoncan.Client(conn, request_timeout=2, config=config) as client:
    try:
        response = client.change_session(udsoncan.DiagnosticSessionControl.DefaultSession)  # 0x10 0x01
        
        if response.positive:
            print("✅ Default Session Activated Successfully!")
        else:
            print(f"❌ Session Change Failed! Response: {response}")
    
    except Exception as e:
        print(f"⚠️ Error: {e}")
