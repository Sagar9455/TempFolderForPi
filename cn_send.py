import can
import time
from datetime import datetime

can_interface="can0"

bus =can.Bus(interface="socketcan",channel=can_interface,bitrate=1000000)

#message=can.Message(arbitration_id=0x9878,data=[0x12,0xBD,0xBE,0xEF,0x02,0x9,0x9,0x5],is_extended_id=False,)
messages=[
can.Message(arbitration_id=0x2314,data=[0xFF,0xBD,0xBE,0xEF,0x03,0x8,0x1,0x6],is_extended_id=False,)
,can.Message(arbitration_id=0x123,data=[0xAA,0xBD,0xBE,0xEF,0x04,0x7,0x2,0x7],is_extended_id=False,)
,can.Message(arbitration_id=0x3458,data=[0xFF,0xAD,0xBE,0xEF,0x05,0x6,0x3,0x8],is_extended_id=False,)
,can.Message(arbitration_id=0x8928,data=[0xEE,0xAD,0xBE,0xEF,0x06,0x5,0x4,0x9],is_extended_id=False,)
]

for msg in messages:
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    bus.send(msg)
    print(f"[{timestamp}] Message sent:ID={hex(msg.arbitration_id)},Data={list(msg.data)}")
    time.sleep(5)


bus.shutdown()
