import csv
'''
def read_and_print_test_cases(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        print("Headers:", headers)
        for row in reader:
            test_id, step, service, subfunction, expected, timeout = row
            print(f"Test ID: {test_id}, Step: {step}, UDS Service: {service}, SubFunction/DataID: {subfunction}, Expected Response: {expected}, Timeout (ms): {timeout}")

if __name__ == "__main__":
    csv_file_path = "UDS_TestCases.csv"  # Change to your actual file path
    read_and_print_test_cases(csv_file_path)

'''

def read_and_print_specific_test_case(csv_file_path, test_case_id):
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        print("Headers:", headers)
        for row in reader:
            test_id, step, service, subfunction, expected, timeout = row
            if test_id == test_case_id:
                print(f"Test ID: {test_id}, Step: {step}, UDS Service: {service}, SubFunction/DataID: {subfunction}, Expected Response: {expected}, Timeout (ms): {timeout}")

if __name__ == "__main__":
    csv_file_path = 'UDS_MultiStep_TestCases.csv'  # Change to your actual file path
    test_case_id = "UDS_TC001"  # Specify the test case ID you want to execute
    read_and_print_specific_test_case(csv_file_path, test_case_id)
