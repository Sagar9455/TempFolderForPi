import udsoncan
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client
import udsoncan.configs
import struct

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
    'default': '>H',  # Default codec is a struct.pack/unpack string (16-bit little endian)
    0x1234: MyCustomCodecThatShiftBy4,  # Custom codec
    0x1235: MyCustomCodecThatShiftBy4(),
    0xF1DD: udsoncan.AsciiCodec(10)  # VIN is 10 bytes long
}

# IsoTP Connection Setup (Ensure you are using the correct CAN interface)
conn = IsoTPSocketConnection('can0', rxid=0x456, txid=0x123)  # Update CAN interface if needed

with Client(conn, request_timeout=2, config=config) as client:
    response = client.read_data_by_identifier([0xF1DD])
    print(response.service_data.values[0xF1DD])  # Print VIN number
    
    # Shortcut to get the VIN directly
    vin = client.read_data_by_identifier_first(0xF1DD)
    print(f"VIN: {vin}")
