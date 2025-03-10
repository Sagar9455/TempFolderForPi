from udsoncan.client import Client
from udsoncan.connections import IsoTPSocketConnection
from udsoncan import AsciiCodec
from udsoncan.exceptions import *

# Configuration for Data Identifiers (DIDs)
custom_config = {
    'data_identifiers': {
        0xF190: AsciiCodec(17)  # VIN is typically 17 characters
    },
    'request_timeout': 2.0,    # Extended timeout for long data
    'p2_timeout': 0.050,      # ECU-specified timing
    'p2_star_timeout': 5.0    # ECU-specified timing for extended periods
}

# Establish ISO-TP connection for CAN communication
conn = IsoTPSocketConnection('can0', rxid=0x18DAF190, txid=0x18DB33F1)

try:
    with Client(conn, config=custom_config) as client:
        # Step 1: Switch to Default Session
        try:
            client.change_session(0x01)  # Default Diagnostic Session
            print("[INFO] Switched to Default Diagnostic Session.")
        except Exception as e:
            print(f"[ERROR] Failed to switch to Default Session: {e}")
            exit()

        # Step 2: Switch to Extended Session
        try:
            client.change_session(0x03)  # Extended Diagnostic Session
            print("[INFO] Switched to Extended Diagnostic Session.")
        except Exception as e:
            print(f"[ERROR] Failed to switch to Extended Session: {e}")
            exit()

        # Step 3: Send Tester Present to maintain session
        try:
            client.tester_present()
            print("[INFO] Tester Present request sent successfully.")
        except Exception as e:
            print(f"[ERROR] Tester Present failed: {e}")

        # Step 4: Read Data By Identifier (RDBI) - Request VIN
        try:
            response = client.read_data_by_identifier(0xF190)
            if response.positive:
                vin = response.service_data.values[0xF190]
                print(f"[INFO] VIN Data: {vin}")
            else:
                print(f"[ERROR] Negative Response Code: {response.code}")
        except NegativeResponseException as e:
            print(f"[ERROR] Negative Response: {e}")
        except TimeoutException as e:
            print(f"[ERROR] Timeout Exception: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")

except Exception as e:
    print(f"[ERROR] Connection Error: {e}")
finally:
    conn.close()
    print("[INFO] Connection Closed.")
