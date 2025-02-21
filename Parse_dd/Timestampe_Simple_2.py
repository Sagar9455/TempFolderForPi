import csv
import datetime
import time

def log_uds_data(entry_type, data, csv_filename='uds_log.csv'):
    timestamp = datetime.datetime.now()
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"), entry_type, data])
    print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')} -> {entry_type}: {data}")

def initialize_csv(csv_filename='uds_log.csv'):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Type', 'Data'])

def main():
    initialize_csv()
    uds_data = [
        ("Request", "0x10 0x01", "Response", "0x50 0x01"),
        ("Request", "0x11 0x01", "Response", "0x51 0x01"),
        ("Request", "0x22 0xF1 0x90", "Response", "0x62 0xF1 0x90 0x12 0x34"),
    ]

    for req_type, req_data, res_type, res_data in uds_data:
        log_uds_data(req_type, req_data)
        time.sleep(0.05)  # Simulating delay
        log_uds_data(res_type, res_data)

if __name__ == "__main__":
    main()
