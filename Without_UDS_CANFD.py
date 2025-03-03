import can
import time

CAN_INTERFACE = "can0"
EXTENDED_CAN_ID = 0x18DAF110  # Change based on your ECU

def send_can_fd_message(arbitration_id, data):
    """Send a CAN FD message with extended ID."""
    try:
        bus = can.interface.Bus(channel=CAN_INTERFACE, bustype="socketcan")
        msg = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=True, is_fd=True)
        bus.send(msg)
        print(f"Sent CAN FD: ID={hex(arbitration_id)} Data={data.hex()} Extended=True")
    except Exception as e:
        print(f"Error sending CAN FD message: {e}")

def receive_can_fd_message(timeout=2):
    """Receive a CAN FD message."""
    try:
        bus = can.interface.Bus(channel=CAN_INTERFACE, bustype="socketcan")
        msg = bus.recv(timeout=timeout)
        if msg:
            print(f"Received CAN FD: ID={hex(msg.arbitration_id)} Data={msg.data.hex()} Extended=True")
        else:
            print("No response received.")
    except Exception as e:
        print(f"Error receiving CAN FD message: {e}")

# 1. Default Session (0x10 0x01)
send_can_fd_message(EXTENDED_CAN_ID, [0x02, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
receive_can_fd_message()
time.sleep(0.1)

# 2. Extended Session (0x10 0x03)
send_can_fd_message(EXTENDED_CAN_ID, [0x02, 0x10, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00])
receive_can_fd_message()
time.sleep(0.1)

# 3. ReadDataByIdentifier (0x22 0xF1 0x90)
send_can_fd_message(EXTENDED_CAN_ID, [0x03, 0x22, 0xF1, 0x90, 0x00, 0x00, 0x00, 0x00])
receive_can_fd_message()
