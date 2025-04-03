import time
import os
import can
import threading


bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000)  # Standard CAN (8-byte frames)
class CANHandler:
	def __init__(self,display_callback):
		 self.display_callback=display_text
		 
		 
		
	def setup_can_interface(self):
		os.system('sudo ip link set can0 type can bitrate 500000')  # Set bitrate to 500kbps
		os.system('sudo ifconfig can0 up')

	def CAN_Send(self,bt):
    messages = {
        12: (0x123, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]),
        16: (0x456, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
        20: (0x789, [0x10, 0xFF, 0x02, 0x03, 0xBC, 0x05, 0x06, 0x07]),
        21: (0x111, [0xFF] * 8),
    }
    if bt in messages:
        msg_id, data = messages[bt]
        msg = can.Message(arbitration_id=msg_id, is_extended_id=False, data=data)
        bus.send(msg)
       #display_text(f"Sent: ID {hex(msg_id)}", y=15)
        self.display_callback(f"Sent:\nID: {hex(msg_id)}\nData:\n{bytes(data).hex()}", y=15)
        
     
    # Function to receive, modify, and respond
    def CAN_Receive_And_Respond(self):
    """Receives CAN message, modifies ID & data, and sends back"""
    while True:
        msg = bus.recv()  # Wait for a message
        if msg:
            received_id = msg.arbitration_id
            data = list(msg.data)

            # Display received message
            self.display_callback(f"Received Message:\nID {hex(received_id)}\nData: {msg.data.hex()}", y=15)
            time.sleep(1)
            # Modify ID and data
            new_id = (received_id + 1) & 0x7FF  # Keep ID within 11-bit range
            new_data = [(b + 1) & 0xFF for b in data]  # Increment data bytes

            # Send modified message
            response_msg = can.Message(arbitration_id=new_id, is_extended_id=False, data=new_data)
            bus.send(response_msg)

            # Display updated message
            self.display_callback(f"Sent:\nID:  {hex(new_id)}\nData: {bytes(new_data).hex()}", y=15)    
            
            
          # Start CAN receiving and responding in a separate thread   
    def start_rx_thread(self):
		rx_thread = threading.Thread(target=CAN_Receive_And_Respond, daemon=True)
		rx_thread.start()
     
  
