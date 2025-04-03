import can
import time
import os
import random

os.system('sudo ip link set can0 type can bitrate 500000')  # Set bitrate to 500kbps
os.system('sudo ifconfig can0 up')
# Dictionary to store counts for received messages
received_count = {}
# Dictionary to store counts for transmitted messages
#transmitted_count = {}

# Initialize CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

def receive_can_messages():
    
    """ Continuously receive CAN messages and count occurrences. """
    print("Listening for CAN messages...")
    last_recevied_time=time.time()
    
    try:
        while True:
            msg = bus.recv(timeout=5)  # Non-blocking
            if msg:
                can_id = msg.arbitration_id  # Extract CAN ID
                
                # Update received message count
                received_count[can_id] = received_count.get(can_id, 0) + 1
                
                # Print real-time message count
                print(f"RX [{hex(can_id)}] Count: {received_count[can_id]}")
                last_recevied_time=time.time()
              
            else:
                  print("\n No messages recevied.\nStopping")
                  break  
    
    except can.CanError:
        print("\nStopped receiving.")
        
       
    finally:
        bus.shutdown()
        print("Final Received Message Counts:")
        for can_id,count in received_count.items():
            print(f"CAN_ID {hex(can_id)}:{count} messages")
        
'''
def send_can_message(can_id, data):
    """ Send a CAN message and track transmission count. """
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

    try:
        bus.send(msg)
        transmitted_count[can_id] = transmitted_count.get(can_id, 0) + 1
        print(f"TX [{hex(can_id)}] Count: {transmitted_count[can_id]}")
    except can.CanError:
        print("Message NOT sent!")
'''
if __name__ == "__main__":
    receive_can_messages()
   
   
   
   
   
   
'''     
    # Start listening for received messages in the background
    import threading
    recv_thread = threading.Thread(target=receive_can_messages, daemon=True)
    recv_thread.start()

    # Send messages in the range 100 to 300
for msg_id in range(100, 301):
    # Generate a random 16-byte data payload (CAN FD supports up to 64 bytes)
    data_bytes = [random.randint(0x00, 0xFF) for _ in range(8)]

    message = can.Message(
        arbitration_id=msg_id, 
        data=data_bytes,
        is_extended_id=False,
        is_fd=False  # Enable CAN FD mode
    )
    
    try:
        bus.send(message)
        print(f"Sent CAN FD message with ID: {msg_id}, Data: {data_bytes}")
    except can.CanError:
        print(f"Failed to send CAN FD message with ID: {msg_id}")
    
    time.sleep(0.01)  # Small delay to avoid flooding

    # Example: Sending messages for testing
    try:
        while True:
            send_can_message(0x123, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88])
            time.sleep(1)  # Send message every second
          
    except KeyboardInterrupt:
        print("\nStopped transmitting.")
        print("Final Transmitted Message Counts:", transmitted_count)
'''  
