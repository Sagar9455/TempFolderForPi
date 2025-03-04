import udsoncan
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client
import udsoncan.configs
import struct
import isotp  # Import isotp for AddressingMode

# Custom Codec for Default DID 0x1234
class MyCustomCodecThatShiftBy4(udsoncan.DidCodec):
    def encode(self, val):
        val = (val << 4) & 0xFFFFFFFF  # Shift left by 4 bits
        return struct.pack('<L', val)  # Little endian, 32-bit value

    def decode(self, payload):
        val = struct.unpack('<L', payload)[0]  # Decode the 32-bit value
        return val >> 4  # Reverse the shift

    def __len__(self):
        return 4  # Encoded payload is 4 bytes long

# UDS Client Configuration
config = dict(udsoncan.configs.default_client_config)
config['data_identifiers'] = {
    'default': '>H',  # Default codec (16-bit little endian)
    0x1234: MyCustomCodecThatShiftBy4,  # Custom codec for default DID
    0xF1DD: udsoncan.AsciiCodec(10)  # VIN is 10 bytes long
}

# Define the CAN Addressing Mode
tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x123, rxid=0x456)

# IsoTP Connection Setup
conn = IsoTPSocketConnection('can0', address=tp_addr)  # Pass the address object

# Start UDS Client
with Client(conn, request_timeout=2, config=config) as client:
    print("Switching to Extended Session (0x10 0x03)...")
    client.change_session(udsoncan.Session.ExtendedDiagnostic)
    print("Extended Session Activated ✅")

    # Read VIN (0xF1DD)
    print("Requesting VIN (DID 0xF1DD)...")
    response = client.read_data_by_identifier([0xF1DD])
    vin = response.service_data.values[0xF1DD]
    print(f"VIN: {vin}")

    # Read Default DID 0x1234
    print("Requesting Default DID 0x1234...")
    response = client.read_data_by_identifier([0x1234])
    default_value = response.service_data.values[0x1234]
    print(f"Default DID Value (0x1234): {default_value}")

    # Switch back to Default Session
    print("Switching back to Default Session (0x10 0x01)...")
    client.change_session(udsoncan.Session.Default)
    print("Default Session Activated ✅")
