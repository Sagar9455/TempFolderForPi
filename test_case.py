import csv
import can
from time import sleep

def send_uds_request(bus, arbitration_id, data):
    msg = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    bus.send(msg)
    print(f"Sent: {msg}")

def parse_and_send_uds_csv(filename):
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            test_id, step, service, subfunction, expected, timeout = row
            service_bytes = [int(b, 16) for b in service.split()]
            sub_bytes = [int(b, 16) for b in subfunction.split() if b.strip()]
            data = service_bytes + sub_bytes
            send_uds_request(bus, 0x7E0, data)
            sleep(int(timeout)/1000)

if __name__ == "__main__":
    csv_file = 'UDS_MultiStep_TestCases.csv'  # Replace with your CSV path
    parse_and_send_uds_csv(csv_file)
