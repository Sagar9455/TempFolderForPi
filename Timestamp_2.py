import can
import csv
import datetime

# Initialize CAN interface
def init_can_interface(channel='can0', bitrate=500000):
    bus = can.interface.Bus(channel=channel, bustype='socketcan', bitrate=bitrate)
    return bus

# Log UDS data with timestamp
def log_uds_data(request_id, data, csv_filename='uds_log.csv'):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, request_id, data])

# Initialize CSV file with headers
def initialize_csv(csv_filename='uds_log.csv'):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'CAN_ID', 'Data'])

# Main loop to read and log CAN messages
def main():
    initialize_csv()
    bus = init_can_interface()

    print("Listening for UDS messages on CAN bus...")
    while True:
        msg = bus.recv()  # Blocking call to receive CAN message
        if msg is not None:
            log_uds_data(hex(msg.arbitration_id), msg.data.hex())
            print(f"Logged: {hex(msg.arbitration_id)} {msg.data.hex()}")

if __name__ == "__main__":
    main()
