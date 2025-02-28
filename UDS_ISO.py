import isotp
import can

# Setup CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Correct ISO-TP Address setup
addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x7E0, rxid=0x7E8)

# Create ISO-TP Stack
stack = isotp.CanStack(bus, address=addr)

# Send a UDS ReadDataByIdentifier (RDBI) request for VIN (0xF190)
stack.send([0x22, 0xF1, 0x90])

# Wait and receive response
response = stack.recv()
if response:
    print(f"Received: {response.hex()}")
else:
    print("No response received.")
