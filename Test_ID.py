import can
import isotp
import udsoncan
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs
import time

# Define ISO-TP parameters
isotp_params = {
    'stmin': 32,                           
    'blocksize': 8,                         
    'wftmax': 0,                            
    'tx_data_length': 8,                    
    'tx_padding': 0xAA,  # Ensure padding byte is 0xAA
    'rx_flowcontrol_timeout': 1000,         
    'rx_consecutive_frame_timeout': 1000,   
    'squash_stmin_requirement': False,      
    'max_frame_size': 4095,                 
    'can_fd': False,                        
    'bitrate_switch': False,                
}

# Copy default UDS client configuration
uds_config = udsoncan.configs.default_client_config.copy()
uds_config["padding_byte"] = 0xAA  # Ensure UDS requests are padded

# Define CAN interface for Raspberry Pi (SocketCAN)
interface = "can0"  # Modify if needed

# Create CAN bus interface
bus = can.interface.Bus(channel=interface, bustype="socketcan", bitrate=500000)

# Define ISO-TP addressing for extended CAN IDs
tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DB33F1, rxid=0x18DAF190)

# Create ISO-TP stack
stack = isotp.NotifierBasedCanStack(bus=bus, address=tp_addr, params=isotp_params)

# Create UDS connection
conn = PythonIsoTpConnection(stack)

# Start UDS Client
with Client(conn, config=uds_config) as client:
    try:
        print("Switching to Extended Diagnostic Session (0x10 0x03)...")
        client.change_session(3)  # Switch to Extended Session
        time.sleep(0.1)  # Small delay to allow ECU to process the session change

        print("Scanning DIDs from 0xF100 to 0xF1FF...\n")

        for i in range(0xF100, 0xF1FF):  # Scan through all potential DIDs
            try:
                response = client.read_data_by_identifier(i)
                print(f"DID 0x{i:X}: {response.service_data.values}")  # Print valid DIDs
            except Exception as e:
                print(f"DID 0x{i:X}: No response or unsupported")
                continue

    except Exception as e:
        print(f"Error: {e}")
