import udsoncan
import isotp
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
from udsoncan.exceptions import *

# Setup logging
udsoncan.setup_logging()

# Define UDS configuration
config = {
    "use_server_timing": True,  # Use ECU timing parameters
    "exception_on_negative_response": False,  # Don't raise exceptions on NRC
}

# Configure ISO-TP connection with 29-bit addressing
conn = PythonIsoTpConnection(
    interface="can0",
    rxid=0x18DAF110,  # ECU response ID
    txid=0x18DAF101,  # Tester request ID
    addressing_mode=isotp.AddressingMode.Normal_29bits  # Use 29-bit CAN identifiers
)

# UDS client
with Client(conn, request_timeout=2, config=config) as client:
    try:
        print("Requesting Extended Diagnostic Session...")
        client.change_session(udsoncan.services.DiagnosticSessionControl.Session.extendedDiagnosticSession)  # Equivalent to 0x03
        print("Extended Diagnostic Session activated.")

    except NegativeResponseException as e:
        print(f"Server refused request for service {e.response.service.get_name()} with code {e.response.code_name} (0x{e.response.code:02x})")

    except (InvalidResponseException, UnexpectedResponseException) as e:
        print(f"Server sent an invalid payload: {e.response.original_payload}")
