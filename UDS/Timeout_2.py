import udsoncan
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs
import struct
import isotp
import can
import time

# Define ISO-TP parameters
isotp_params = {
    'stmin': 32,
    'blocksize': 8,
    'wftmax': 0,
    'tx_data_length': 8,
    'tx_padding': 0xAA,  # Ensure padding is applied
    'rx_flowcontrol_timeout': 1000,
    'rx_consecutive_frame_timeout': 1000,
    'squash_stmin_requirement': False,
    'max_frame_size': 4095,
    'can_fd': False,
}

# UDS Client Configuration
config = dict(udsoncan.configs.default_client_config)
config["padding_byte"] = 0xAA
config["p2_timeout"] = 0.100  # Set initial P2 timeout to 100ms (instead of 50ms)
config["p2_star_timeout"] = 5.0
config["request_timeout"] = 3  # Increase request timeout

# Define CAN interface for Raspberry Pi (SocketCAN)
interface = "can0"
bus = can.interface.Bus(channel=interface, bustype="socketcan", bitrate=500000)

# Define ISO-TP addressing for extended CAN IDs
tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DB33F1, rxid=0x18DAF190)

# Create ISO-TP stack
stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)

# Create UDS connection
conn = PythonIsoTpConnection(stack)

# Start UDS Client
with Client(conn, request_timeout=3, config=config) as client:
    try:
        print("Switching to Extended Diagnostic Session (0x10 0x03)...")
        response = client.change_session(0x03)

        # Extract P2 and P2* timing values
        if response.service_data is not None and len(response.service_data.data) >= 5:
            p2_high = response.service_data.data[1]
            p2_low = response.service_data.data[2]
            p2_star_high = response.service_data.data[3]
            p2_star_low = response.service_data.data[4]

            # Convert to seconds
            new_p2_timeout = max(((p2_high << 8) + p2_low) / 1000, 0.1)  # Ensure at least 100ms
            new_p2_star_timeout = max((((p2_star_high << 8) + p2_star_low) * 10) / 1000, 5)

            print(f"Updating P2 Timeout to {new_p2_timeout}s, P2* Timeout to {new_p2_star_timeout}s")

            client.config["p2_timeout"] = new_p2_timeout
            client.config["p2_star_timeout"] = new_p2_star_timeout
            client.config["request_timeout"] = max(new_p2_timeout * 2, 3)  # Ensure minimum timeout

        time.sleep(0.5)

        print("Sending Tester Present to keep session alive...")
        client.tester_present(0x00)

        print("Reading Data Identifier 0xF190 (VIN)...")
        response = client.read_data_by_identifier(0xF190)
        print(f"VIN: {response.service_data.values[0xF190]}")

    except Exception as e:
        print(f"Error: {e}")
