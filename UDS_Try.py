import can
import isotp
import time

# Define Tx and Rx CAN IDs based on your CANoe configuration
TX_ID = 0x1A30C0B1  # Request ID (ECU Address)
RX_ID = 0x1A30CB10  # Response ID (ECU Reply Address)

# Setup CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan', fd=False)  # CAN FD disabled

# Setup ISO-TP protocol with extended 29-bit CAN IDs
addr = isotp.Address(rxid=RX_ID, txid=TX_ID, is_extended_id=True)
stack = isotp.TransportLayer(bus=bus, address=addr)

# Function to send a UDS request and wait for response
def send_uds_request(request_bytes, description):
    stack.send(request_bytes)
    print(f"{description} Sent: {request_bytes.hex()}")
    
    time.sleep(0.5)  # Allow time for ECU response
    response = stack.recv()

    if response:
        print(f"Response: {response.hex()}")
        return response
    else:
        print("No response received")
        return None

# Step 1: Try switching to Extended Diagnostic Session
session_request = bytes([0x10, 0x03])  # 0x10 = DiagnosticSessionControl, 0x03 = Extended Session
session_response = send_uds_request(session_request, "Extended Session Request")

# Check if session switch was successful
if session_response and session_response[:2] == bytes([0x50, 0x03]):
    print("ECU switched to Extended Diagnostic Session successfully.")

else:
    print("Extended Session Request failed. Trying Default Session first...")
    
    # Step 1.1: Send Default Session Request
    default_session_request = bytes([0x10, 0x01])  # 0x10 = DiagnosticSessionControl, 0x01 = Default Session
    default_response = send_uds_request(default_session_request, "Default Session Request")
    
    if default_response and default_response[:2] == bytes([0x50, 0x01]):  # 0x50 0x01 means Default Session accepted
        print("ECU switched to Default Session. Retrying Extended Session...")
        
        # Retry Extended Session Request
        session_response = send_uds_request(session_request, "Extended Session Request (Retry)")
        
        if not session_response or session_response[:2] != bytes([0x50, 0x03]):
            print("Extended Session Request still failed. Aborting VIN request.")
            exit()

# Step 2: Send UDS ReadDataByIdentifier request for VIN (DID 0xF190)
vin_request = bytes([0x22, 0xF1, 0x90])  # 0x22 = ReadDataByIdentifier, 0xF190 = VIN
vin_response = send_uds_request(vin_request, "VIN Read Request")

# Step 3: Decode VIN if response is positive
if vin_response and vin_response[:3] == bytes([0x62, 0xF1, 0x90]):  # 0x62 = Positive response
    vin = ''.join(chr(byte) for byte in vin_response[3:])  # Convert bytes to ASCII
    print(f"VIN Number: {vin}")
else:
    print("VIN Request failed or negative response received.")
