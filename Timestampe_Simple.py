import csv
import datetime

# Function to log data with timestamp
def log_data(data, csv_filename='timestamp_test.csv'):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Current timestamp with milliseconds
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, data])

# Initialize CSV with headers
def initialize_csv(csv_filename='timestamp_test.csv'):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Data'])

# Main function
def main():
    initialize_csv()
    test_data = ["Data 1", "Data 2", "Data 3", "Data 4", "Data 5"]  # Sample data

    for item in test_data:
        log_data(item)
        print(f"Logged: {item}")

if __name__ == "__main__":
    main()
