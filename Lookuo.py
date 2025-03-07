import can
import time

# Dictionary to store counts for received messages
received_count = {}
# Dictionary to store counts for transmitted messages
transmitted_count = {}

# Initialize CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

def receive_can_messages():
    """ Continuously receive CAN messages and count occurrences. """
    print("Listening for CAN messages... Press Ctrl+C to stop.")
    
    try:
        while True:
            msg = bus.recv(timeout=1)  # Non-blocking
            if msg:
                can_id = msg.arbitration_id  # Extract CAN ID
                
                # Update received message count
                received_count[can_id] = received_count.get(can_id, 0) + 1
                
                # Print real-time message count
                print(f"RX [{hex(can_id)}] Count: {received_count[can_id]}")
    
    except KeyboardInterrupt:
        print("\nStopped receiving.")
        print("Final Received Message Counts:", received_count)

def send_can_message(can_id, data):
    """ Send a CAN message and track transmission count. """
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

    try:
        bus.send(msg)
        transmitted_count[can_id] = transmitted_count.get(can_id, 0) + 1
        print(f"TX [{hex(can_id)}] Count: {transmitted_count[can_id]}")
    except can.CanError:
        print("Message NOT sent!")

if __name__ == "__main__":
    # Start listening for received messages in the background
    import threading
    recv_thread = threading.Thread(target=receive_can_messages, daemon=True)
    recv_thread.start()

    # Example: Sending messages for testing
    try:
        while True:
            send_can_message(0x123, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88])
            time.sleep(1)  # Send message every second
    except KeyboardInterrupt:
        print("\nStopped transmitting.")
        print("Final Transmitted Message Counts:", transmitted_count)
