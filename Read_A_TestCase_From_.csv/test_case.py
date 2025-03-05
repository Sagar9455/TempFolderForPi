import csv

def read_and_print(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        print(headers)
        for row in reader:
            test_id   , step, service, subfunction, expected, timeout = row
            print(f"TestID:{test_id}, Step{step},UDS Service:{ service}, Subfunction:{subfunction},ExpectedResponse:{ expected}, Timeout(ms):{timeout}")

csv_file = 'UDS_MultiStep_TestCases.csv' 
read_and_print(csv_file)
