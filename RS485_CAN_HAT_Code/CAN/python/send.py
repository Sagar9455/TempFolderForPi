import os
import can
'''
os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
can0.send(msg)

os.system('sudo ifconfig can0 down')

'''
os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

#can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

bus = can.Bus(interface = 'socketcan',channel='can0',bitrate=1000000)
msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
bus.send(msg)
print("Message sent")
bus.shutdown


#os.system('sudo ifconfig can0 down')

