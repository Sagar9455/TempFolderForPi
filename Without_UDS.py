import can

bus = can.interface.Bus(channel='can0', bustype='socketcan')

msg_tx = can.Message(arbitration_id=0x7E0, data=[0x10, 0x01], is_extended_id=False)
print(f"Sending TX: ID={hex(msg_tx.arbitration_id)}, DATA={msg_tx.data.hex()}")
bus.send(msg_tx)

msg_rx = bus.recv(5.0)  
if msg_rx:
    print(f"Received RX: ID={hex(msg_rx.arbitration_id)}, DATA={msg_rx.data.hex()}")
else:
    print("No response received.")
