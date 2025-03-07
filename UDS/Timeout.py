import time
import can
import isotp
import udsoncan
from udsoncan.connections import IsoTPConnection
from udsoncan.client import Client
import logging
import os


os.system('sudo ip link set can0 type can bitrate 500000')  # Set bitrate to 500kbps
os.system('sudo ifconfig can0 up')

logging.basicConfig(level=logging.DEBUG)
udsoncan.setup_logging()
# CAN setup

interface = "can0"

# Create CAN bus interface
bus = can.interface.Bus(channel=interface, bustype="socketcan", bitrate=500000)
tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DA34FA, rxid=0x18DAFA34)

tp_layer = isotp.CanStack(
    bus=bus,
    address=tp_addr,
    params={
        "stmin": 0,
        "blocksize": 0,
        "tx_data_length": 8
    }
)

conn = IsoTPConnection(tp_layer)

# Set correct timeouts
client_config = {
    "request_timeout": 5,      # Max wait time
    "p2_timeout": 1.0,         # Increase P2 timeout (default was 50ms)
    "p2_star_timeout": 5.0     # Increase extended timeout
}

with Client(conn, **client_config) as uds_client:
    try:
        print("Switching to Extended Diagnostic Session...")
        uds_client.diagnostic_session_control(0x03)
        time.sleep(0.5)

        print("Sending ReadDataByIdentifier (0x22F1DD)...")
        response = uds_client.read_data_by_identifier(0xF1DD)
        print(f"Response: {response}")

    except Exception as e:
        print(f"Error: {e}")
