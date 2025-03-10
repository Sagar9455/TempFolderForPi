import can
import isotp
import time

# ISO-TP Configuration with Padding
isotp_params = {
    'stmin': 32,
    'blocksize': 8,
    'wftmax': 0,
    'tx_data_length': 8,
    'tx_padding': 0x00,   # PADDING ENABLED
    'rx_flowcontrol_timeout': 1000,
    'rx_consecutive_frame_timeout': 1000
}

# ISO-TP Addressing
tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DB33F1, rxid=0x18DAF190)

# Create CAN Bus Interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# Create ISO-TP Stack with Padding
stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)

# Send RDBI Request (0x22 0xF1 0x90) with Padding
rdbi_request = bytes([0x22, 0xF1, 0x90])  # RDBI request for DID 0xF190
stack.send(rdbi_request)

# Read and Print Response
response = stack.recv(timeout=2)
if response:
    print(f"Response Received: {response.hex().upper()}")
else:
    print("No Response Received")
