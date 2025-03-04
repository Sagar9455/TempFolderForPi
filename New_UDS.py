import can
import isotp
import udsoncan
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs

# Define ISO-TP parameters
isotp_params = {
    'stmin': 32,                          
    'blocksize': 8,                         
    'wftmax': 0,                            
    'tx_data_length': 8,                     
    'tx_data_min_length': None,              
    'tx_padding': 0xAA,  # Set padding to 0xAA as requested
    'rx_flowcontrol_timeout': 1000,         
    'rx_consecutive_frame_timeout': 1000,   
    'squash_stmin_requirement': False,      
    'max_frame_size': 4095,                 
    'can_fd': False,                        
    'bitrate_switch': False,                
    'rate_limit_enable': False,             
    'rate_limit_max_bitrate': 1000000,      
    'rate_limit_window_size': 0.2,          
    'listen_mode': False,                   
}

# Copy default UDS client configuration
uds_config = udsoncan.configs.default_client_config.copy()
uds_config["padding_byte"] = 0xAA  # Ensure padding is applied in UDS

# Define CAN interface for Raspberry Pi (SocketCAN)
interface = "can0"  # Make sure this matches your Raspberry Pi setup

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
    client.change_session(1)  # 0x10 0x01 - Default Diagnostic Session
