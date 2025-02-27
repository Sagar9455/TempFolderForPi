import can
import time
from datetime import datetime

can_interface="can0"

bus =can.Bus(interface="socketcan",channel=can_interface,bitrate=1000000)

while True:
    msg = bus.recv()
    print (msg)


