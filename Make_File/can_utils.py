import os
import can
import threading
import time

class CANHandler:
    def __init__(self, display_callback):
        self.display_callback = display_callback
        self.bus = None
        self.setup_can_interface()

    def setup_can_interface(self):
        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ifconfig can0 up')
        self.bus = can.Bus(interface="socketcan", channel="can0", bitrate=500000)

    def send_can_message(self, btn):
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
        while True:
            msg = self.bus.recv()  # Wait for a message
            if msg:
                received_id = msg.arbitration_id
                data = list(msg.data)

                self.display_callback(f"Received:\nID {hex(received_id)}\nData: {msg.data.hex()}")
                time.sleep(1)

                new_id = (received_id + 1) & 0x7FF
                new_data = [(b + 1) & 0xFF for b in data]

                response_msg = can.Message(arbitration_id=new_id, is_extended_id=False, data=new_data)
                self.bus.send(response_msg)

                self.display_callback(f"Sent:\nID: {hex(new_id)}\nData: {bytes(new_data).hex()}")

    def start_rx_thread(self):
        threading.Thread(target=self.receive_and_respond, daemon=True).start()
