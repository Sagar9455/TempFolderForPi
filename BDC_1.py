import can
import logging
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs
import isotp

# Logging setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# Define ISO-TP parameters
isotp_params = {
    'stmin': 32,
    'blocksize': 8,
    'wftmax': 0,
    'tx_data_length': 8,
    'tx_padding': None,  # No padding (important for your case)
    'rx_flowcontrol_timeout': 1000,
    'rx_consecutive_frame_timeout': 1000,
    'squash_stmin_requirement': False,
    'max_frame_size': 4095,
    'can_fd': False  # Standard CAN
}

# UDS Client Configuration
config = dict(udsoncan.configs.default_client_config)
config["ignore_server_timing_requirements"] = True
config["padding_byte"] = None  # No padding byte

# Define CAN interface
interface = "can0"

# Create CAN bus interface
bus = can.interface.Bus(channel=interface, bustype="socketcan", bitrate=500000)

# Define ISO-TP addressing for 11-bit CAN IDs
tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x8A0, rxid=0x8A8)

# Create ISO-TP stack
stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)

# Create UDS connection
conn = PythonIsoTpConnection(stack)

# Send raw UDS request (without PCI byte)
try:
    with Client(conn, request_timeout=2, config=config) as client:
        logging.info("UDS Client Started")

        # Send raw UDS request directly
        conn.send(bytes([0x22, 0xF1, 0x90]))  # Raw UDS request
        logging.info("Sent: 22 F1 90")

        # Receive and log response
        response = conn.wait_frame(timeout=2)  
        if response:
            logging.info(f"Received: {response.hex()}")
        else:
            logging.warning("No response received")

except Exception as e:
    logging.error(f"Error: {e}")
