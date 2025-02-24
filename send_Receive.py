import can
import time
import threading

# Configure CAN interface
can_interface = "can0"
bus = can.interface.Bus(channel=can_interface, bustype="socketcan")

def send_periodic_messages(delay):
    """Sends messages at a fixed interval"""
    msg_id = 0x100  # Example ID
    data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

    while True:
        message = can.Message(arbitration_id=msg_id, data=data, is_extended_id=False)
        try:
            bus.send(message)
            print(f"Sent: {message}")
        except can.CanError:
            print("Message NOT sent")
        time.sleep(delay)

def receive_and_respond():
    """Receives messages, modifies data, and sends with a new ID"""
    while True:
        msg = bus.recv()  # Blocking receive
        if msg:
            print(f"Received: {msg}")

            # Modify Data (Increment each byte)
            new_data = [(b + 1) & 0xFF for b in msg.data]  # Ensure it stays within byte range

            # Send new message with different ID
            new_id = msg.arbitration_id + 1
            response = can.Message(arbitration_id=new_id, data=new_data, is_extended_id=False)
            try:
                bus.send(response)
                print(f"Sent Response: {response}")
            except can.CanError:
                print("Response NOT sent")

# Create threads for both tasks
tx_thread = threading.Thread(target=send_periodic_messages, args=(0.01,))  # 10ms delay
rx_thread = threading.Thread(target=receive_and_respond)

# Start threads
tx_thread.start()
rx_thread.start()

# Keep the main thread running
tx_thread.join()
rx_thread.join()
