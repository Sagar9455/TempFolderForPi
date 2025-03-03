import logging
import can
import isotp
import udsoncan
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
from udsoncan.exceptions import *

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)
udsoncan.setup_logging()

# ✅ Step 1: Configure ISO-TP Parameters
isotp_params = {
    "stmin": 5,      # Minimum separation time (ms) (Try 0 or 5)
    "blocksize": 8,  # Max frames before ECU waits for FlowControl
    "wftmax": 0,     # Max "wait frame" transmissions
}

# ✅ Step 2: Create CAN Bus Interface
bus = can.interface.Bus(channel="can0", bustype="socketcan")

# ✅ Step 3: Create ISO-TP Stack with 29-bit CAN IDs
stack = isotp.CanStack(
    bus=bus,
    address=isotp.Address(
        rxid=0x18DAF110,  # ECU response ID
        txid=0x18DAF101,  # Tester request ID
        addressing_mode=isotp.AddressingMode.Normal_29bits,  # Use 29-bit IDs
    ),
    params=isotp_params
)

# ✅ Step 4: Create `PythonIsoTpConnection`
conn = PythonIsoTpConnection(stack)

# ✅ Step 5: Open Connection Before Sending Data
print("📡 Opening ISO-TP connection...")
conn.open()  # ✅ REQUIRED: Open the connection before sending

try:
    # ✅ Step 6: Send Raw UDS Frame for Extended Session (0x10 0x03)
    print("📡 Sending raw UDS frame: Extended Diagnostic Session request (0x10 0x03)")
    conn.send(b"\x10\x03")  # Send raw bytes

    # ✅ Step 7: Wait for ECU Response
    response = conn.wait_frame(timeout=2)
    if response:
        print(f"✅ ECU Response: {response.hex()}")
    else:
        print("❌ No response received from ECU.")

finally:
    conn.close()  # ✅ Always close the connection when done

# ✅ Step 8: Start UDS Client and Send Extended Session Request
config = {
    "use_server_timing": True,  # Use ECU timing
    "exception_on_negative_response": False,  # Don't throw exceptions on NRCs
}

with Client(conn, request_timeout=2, config=config) as client:
    try:
        print("🚀 Requesting Extended Diagnostic Session (0x10 0x03) via UDS Client...")
        client.change_session(udsoncan.services.DiagnosticSessionControl.Session.extendedDiagnosticSession)
        print("✅ Extended Diagnostic Session activated.")

    except NegativeResponseException as e:
        print(f"❌ Server refused service {e.response.service.get_name()} with code {e.response.code_name} (0x{e.response.code:02x})")

    except (InvalidResponseException, UnexpectedResponseException) as e:
        print(f"❌ Server sent an invalid payload: {e.response.original_payload}")

