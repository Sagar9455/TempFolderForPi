import can
import time
import random

# Configure CAN FD interface
can_interface = "can0"

# Create a CAN bus instance for CAN FD
bus = can.interface.Bus(channel=can_interface, bustype="socketcan", fd=True)

# Send messages in the range 100 to 300
for msg_id in range(100, 301):
    # Generate a random 16-byte data payload (CAN FD supports up to 64 bytes)
    data_bytes = [random.randint(0x00, 0xFF) for _ in range(16)]

    message = can.Message(
        arbitration_id=msg_id, 
        data=data_bytes,
        is_extended_id=False,
        is_fd=True  # Enable CAN FD mode
    )
    
    try:
        bus.send(message)
        print(f"Sent CAN FD message with ID: {msg_id}, Data: {data_bytes}")
    except can.CanError:
        print(f"Failed to send CAN FD message with ID: {msg_id}")
    
    time.sleep(0.01)  # Small delay to avoid flooding

print("CAN FD message transmission completed.")
