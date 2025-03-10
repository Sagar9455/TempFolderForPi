import can
import time

# Create CAN Bus Interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# RDBI Request Frame (with Padding)
rdbi_request = can.Message(
    arbitration_id=0x18DB33F1,
    data=[0x22, 0xF1, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00],  # Padded with 0x00
    is_extended_id=True
)

# Send the RDBI Request
bus.send(rdbi_request)
print("RDBI Request Sent")

# Read Response
while True:
    response = bus.recv(timeout=2)
    if response and response.arbitration_id == 0x18DAF190:
        print(f"Response Received: {response.data.hex().upper()}")
        break
    else:
        print("No Response Received")
        break
