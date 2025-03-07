import udsoncan
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs
import struct
import isotp
import can
import logging

logging.basicConfig(level=logging.DEBUG)
udsoncan.setup_logging()

# Define ISO-TP parameters
isotp_params = {
    'stmin': 32,
    'blocksize': 8,
    'wftmax': 0,
    'tx_data_length': 8,
    'tx_data_min_length': None,
    'tx_padding': 0xAA,  # Set padding to 0xAA
    'rx_flowcontrol_timeout': 1000,
    'rx_consecutive_frame_timeout': 1000,
    'max_frame_size': 4095,
    'can_fd': False,
    'bitrate_switch': False,
    'rate_limit_enable': False,
    'rate_limit_max_bitrate': 1000000,
    'rate_limit_window_size': 0.2,
    'listen_mode': False,
}

# UDS Client Configuration
config = dict(udsoncan.configs.default_client_config)
config['data_identifiers'] = {
    'default': '>H',  # Default codec is a struct.pack/unpack string (16-bit little endian)
    0xF1DD: udsoncan.AsciiCodec(15)  # VIN is 15 bytes long
}
config["padding_byte"] = 0xAA  # Ensure padding is applied in UDS

# Define CAN interface for Raspberry Pi (SocketCAN)
interface = "can0"

# Create CAN bus interface
bus = can.interface.Bus(channel=interface, bustype="socketcan", bitrate=500000)

# Define ISO-TP addressing for extended CAN IDs
tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DA34FA, rxid=0x18DAFA34)

# Create ISO-TP stack
stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)

# Create UDS connection
conn = PythonIsoTpConnection(stack)

# Start UDS Client
with Client(conn, request_timeout=5, config=config) as client:
    # Switch to Extended Session (0x10 0x01)
    client.change_session(3)
    print("Switched to Extended Session")
    
    # Read VIN from DID 0xF1DD with padding
    response = client.read_data_by_identifier(0xF187)
    print(f"VIN: {response.service_data.values[0xF187]}")
