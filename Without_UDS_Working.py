import can
import time
import os

os.system('sudo ip link set can0 type can bitrate 500000')  # Set bitrate to 500kbps
os.system('sudo ifconfig can0 up')


bus = can.interface.Bus(channel='can0', bustype='socketcan')

request=can.Message(arbitration_id=0x18DA34FA, data=[0x02, 0x10, 0x01, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], is_extended_id=True)
bus.send(request)
time.sleep(0.5)
request=can.Message(arbitration_id=0x18DA34FA, data=[0x02, 0x10, 0x03, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], is_extended_id=True)
bus.send(request)
time.sleep(0.5)
request=can.Message(arbitration_id=0x18DA34FA, data=[0x03, 0x22, 0xF1, 0xA0, 0xAA, 0xAA, 0xAA, 0xAA], is_extended_id=True)
bus.send(request)
time.sleep(0.5)
#request=can.Message(arbitration_id=0x18DA34FA, data=[0x02, 0x10, 0x03, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], is_extended_id=True)
#request=can.Message(arbitration_id=0x18DA34FA, data=[0x02, 0x10, 0x03, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], is_extended_id=True)

#time.sleep(0.5)
#request=can.Message(arbitration_id=0x18DA34FA, data=[0x02, 0x10, 0x03, 0xAA, 0xCC, 0xCC, 0xAA, 0xAA], is_extended_id=True)
#bus.send(request)
#time.sleep(1)
#request=can.Message(arbitration_id=0x18DA34FA, data=[0x03, 0x22, 0xF1, 0x90, 0xAA, 0xAA, 0xAA, 0xAA], is_extended_id=True)
#bus.send(request)
response=bus.recv()

if response:
    print("Default session")
    
else:
    print("ERROR")
'''
bus = can.interface.Bus(channel='can0', bustype='socketcan')

msg_tx = can.Message(arbitration_id=0x18DA34FA, data=[0x10, 0x01], is_extended_id=False)
print(f"Sending TX: ID={hex(msg_tx.arbitration_id)}, DATA={msg_tx.data.hex()}")
bus.send(msg_tx)

msg_rx = bus.recv(5.0)  
if msg_rx:
    print(f"Received RX: ID={hex(msg_rx.arbitration_id)}, DATA={msg_rx.data.hex()}")
else:
    print("No response received.")
'''
