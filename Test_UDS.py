import udsoncan
from udsoncan.connections import IsoTPSocketConnection

# Define the connection parameters
conn = IsoTPSocketConnection('can0', rxid=0x7E8, txid=0x7E0)

# Create a client instance
with udsoncan.UdsClient(conn, request_timeout=2) as client:
    # Start a diagnostic session
    client.change_session(udsoncan.services.DiagnosticSessionControl.Session.defaultSession)
    
    # Example: Read ECU Identification
    response = client.read_data_by_identifier(udsoncan.services.ReadDataByIdentifier.DataIdentifier.VIN)
    print(f"Vehicle Identification Number (VIN): {response.data.hex()}")

    # Example: Clear Diagnostic Information
    client.clear_diagnostic_information(0xFFFFFF)

    # Example: Read DTCs (Diagnostic Trouble Codes)
    dtc_response = client.get_dtc_by_status_mask(0xFF)
    for dtc in dtc_response.service_data.dtcs:
        print(f"DTC: {dtc}")

# Connection is automatically closed when exiting the 'with' block
