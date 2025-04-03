import isotp
import can
from udsoncan.client import Client
from udsoncan.connections import IsoTPSocketConnection
#from udsoncan.configs import default_config
from udsoncan.services import DiagnosticSessionControl
import os

os.system('sudo ip link set can0 type can bitrate 500000')  # Set bitrate to 500kbps
os.system('sudo ifconfig can0 up')

bus = can.Bus(interface="socketcan", channel="can0", bitrate=500000)  # Standard CAN (8-byte frames)

# UDS Configuration (Define VIN DID)
'''
config = default_config.copy()
config["data_identifiers"] = {
    0xF190: "vin"  # Define VIN DID
}
'''
config = {
    "data_identifiers": {
         0xF190: "vin"  # Define VIN DID
       }
}
# Setup CAN bus with ISO-TP addressing
conn = IsoTPSocketConnection('can0', isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DA34FA  , rxid=0x18DAFA34))



with Client(conn, request_timeout=2, config=config) as client:
    try:
        #Step 1: Switch to Default Session (0x01)
        client.change_session(DiagnosticSessionControl.Session.defaultSession)
        print("Switched to Default Session")
        print(f"Raw response data: {response.data.hex()}")
        

        #  Step 2: Switch to Extended Diagnostic Session (0x03)
#        client.change_session(DiagnosticSessionControl.Session.extendedDiagnosticSession)
#        print("Switched to Extended Diagnostic Session")

        #  Step 3: Read Current VIN
#        vin_data = client.read_data_by_identifier(0xF190)  # Read VIN (DID 0xF190)
#        vin = vin_data.decode("utf-8")  # Convert bytes to string
#        print(f"Current VIN: {vin}")

    except Exception as e:
        print(f"Error: {e}")




