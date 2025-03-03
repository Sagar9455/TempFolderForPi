import can
import udsoncan
from udsoncan.client import Client
from udsoncan.transport import CanTransport
from udsoncan.connections import PythonIsoTpConnection
import isotp

# Configure CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')
stack = isotp.CanStack(
    bus=bus,
    address=isotp.Address(rxid=0x18DAF110, txid=0x18DA10F1, ext_address=None, addressing_mode=isotp.AddressingMode.Extended)
)
connection = PythonIsoTpConnection(stack)

# UDS client setup
with Client(connection, request_timeout=2) as client:
    try:
        print("Requesting Default Diagnostic Session...")
        client.change_session(udsoncan.services.DiagnosticSessionControl.Session.defaultSession)
        print("Default Session Activated.")
        
        print("Requesting Extended Diagnostic Session...")
        client.change_session(udsoncan.services.DiagnosticSessionControl.Session.extendedDiagnosticSession)
        print("Extended Session Activated.")
    
    except Exception as e:
        print(f"Error: {e}")
