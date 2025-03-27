import os
import can
import threading
import time
import logging

# Logging setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

class CANHandler:
    def __init__(self, display_callback):
        self.display_callback = display_callback  # Reference to OLED display function
        self.bus = None

    def setup_can_interface(self):
        """Setup CAN interface directly in the code"""
        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ifconfig can0 up')
        self.bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000)

    def send_can_message(self, btn):
        """Send CAN message based on button pressed"""
        messages = {
            12: (0x123, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]),
            16: (0x456, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
            20: (0x789, [0x10, 0xFF, 0x02, 0x03, 0xBC, 0x05, 0x06, 0x07]),
            21: (0x111, [0xFF] * 8),
        }
        if btn in messages:
            msg_id, data = messages[btn]
            msg = can.Message(arbitration_id=msg_id, is_extended_id=False, data=data)
            self.bus.send(msg)
            self.display_callback(f"Sent:\nID: {hex(msg_id)}\nData:\n{bytes(data).hex()}")

    def receive_and_respond(self):
        """Receives CAN message, modifies ID & data, and sends back"""
        while True:
            msg = self.bus.recv()  # Wait for a message
            if msg:
                received_id = msg.arbitration_id
                data = list(msg.data)

                # Display received message
                self.display_callback(f"Received:\nID {hex(received_id)}\nData: {msg.data.hex()}")
                time.sleep(1)

                # Modify ID and data
                new_id = (received_id + 1) & 0x7FF
                new_data = [(b + 1) & 0xFF for b in data]

                # Send modified message
                response_msg = can.Message(arbitration_id=new_id, is_extended_id=False, data=new_data)
                self.bus.send(response_msg)

                # Display updated message
                self.display_callback(f"Sent:\nID: {hex(new_id)}\nData: {bytes(new_data).hex()}")

    def start_rx_thread(self):
        """Start a separate thread to handle CAN reception and response"""
        rx_thread = threading.Thread(target=self.receive_and_respond, daemon=True)
        rx_thread.start()