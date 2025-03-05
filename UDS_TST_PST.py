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
    'tx_data_length': 8,
    'tx_padding': 0xAA,
    'rx_flowcontrol_timeout': 2000,
    'rx_consecutive_frame_timeout': 2000,
    'can_fd': False,
}

# UDS Client Configuration
uds_config = udsoncan.configs.default_client_config.copy()
uds_config["padding_byte"] = 0xAA
uds_config["p2_timeout"] = 2
uds_config["p2_star_timeout"] = 5
uds_config["exception_on_invalid_response"] = False
uds_config["data_identifiers"] = {"default": ">H"}

# Setup CAN Bus
interface = "can0"
bus = can.interface.Bus(channel=interface, bustype="socketcan", bitrate=500000)

# ISO-TP Addressing
tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DAF190, rxid=0x18DAF1F1)
stack = isotp.NotifierBasedCanStack(bus=bus, address=tp_addr, params=isotp_params)

# Create UDS connection
conn = PythonIsoTpConnection(stack)

# Start UDS Client
with Client(conn, config=uds_config) as client:
    try:
        print("Switching to Default Diagnostic Session (0x10 0x01)...")
        client.change_session(0x01)
        time.sleep(0.5)

        print("Sending Tester Present to keep session active...")
        client.send_request(udsoncan.services.TesterPresent())
        time.sleep(0.5)

        print("Switching to Extended Diagnostic Session (0x10 0x03)...")
        client.change_session(0x03)
        time.sleep(0.5)

        print("Requesting DID 0xF1DD (ReadDataByIdentifier)...")
        vin_response = client.read_data_by_identifier(0xF1DD)
        print(f"Response: {vin_response.service_data.values}")

    except Exception as e:
        print(f"Error: {e}")
