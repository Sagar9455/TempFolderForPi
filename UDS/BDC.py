import udsoncan
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs
import isotp
import can
import logging
import time
import os


os.system('sudo ip link set can0 type can bitrate 500000')  # Set bitrate to 500kbps
os.system('sudo ifconfig can0 up')

# Logging setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# Define ISO-TP parameters
isotp_params = {
    'stmin': 32,
    'blocksize': 8,
    'wftmax': 0,
    'tx_data_length': 8,
    'tx_padding': None,
    'rx_flowcontrol_timeout': 1000,
    'rx_consecutive_frame_timeout': 1000,
    'max_frame_size': 4095,
    'can_fd': False
}

# UDS Client Configuration
config = dict(udsoncan.configs.default_client_config)
config["ignore_server_timing_requirements"] = True
config["padding_byte"] = None
config["data_identifiers"] = {
    0xF100: udsoncan.AsciiCodec(20),  
    0xF101: udsoncan.AsciiCodec(8),
    0xF187: udsoncan.AsciiCodec(13)
}

# Define CAN interface
interface = "can0"

# Create CAN bus interface
bus = can.interface.Bus(channel=interface, bustype="socketcan", bitrate=500000)

# Define ISO-TP addressing for extended CAN IDs
tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x7A0, rxid=0x7A8)

# Create ISO-TP stack
stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)

# Create UDS connection
conn = PythonIsoTpConnection(stack)

# Start UDS Client
with Client(conn, request_timeout=2, config=config) as client:
    logging.info("UDS Client Started")

    # Tester Present (0x3E)
    try:
        client.tester_present()
        logging.info("Tester Present sent successfully")
    except Exception as e:
        logging.warning(f"Tester Present failed: {e}")

    # Default Session (0x10 0x01)
    try:
        response = client.change_session(0x01)
        if response.positive:
            logging.info("Switched to Default Session")
        else:
            logging.warning("Failed to switch to Default Session")
    except Exception as e:
        logging.error(f"Error in Default Session: {e}")

    # Extended Session (0x10 0x03)
    try:
        response = client.change_session(0x03)
        if response.positive:
            logging.info("Switched to Extended Session")
        else:
            logging.warning("Failed to switch to Extended Session")
    except Exception as e:
        logging.error(f"Error in Extended Session: {e}")

    # Read VIN (DID 0xF190)
    try:
        response = client.read_data_by_identifier(0xF100)
        if response.positive:
            logging.info(f"VIN: {response.service_data.values[0xF100]}")
        else:
            logging.warning("Failed to Read VIN")
    except Exception as e:
        logging.error(f"Error reading VIN: {e}")
       
       
    try:
        time.sleep(0.5)
        response = client.read_data_by_identifier(0xF101)
        if response.positive:
            logging.info(f"VIN: {response.service_data.values[0xF101]}")
        else:
            logging.warning("Failed to Read VIN")
    except Exception as e:
        logging.error(f"Error reading VIN: {e}")

    try:
        time.sleep(0.5)
        response = client.read_data_by_identifier(0xF187)
        if response.positive:
            logging.info(f"VIN: {response.service_data.values[0xF187]}")
        else:
            logging.warning("Failed to Read VIN")
    except Exception as e:
        logging.error(f"Error reading VIN: {e}")
logging.info("UDS Client Closed")
