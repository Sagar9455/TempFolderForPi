'''
def parse_hex(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("S"):
                byte_count = int(line[1:3], 16)
                address = line[3:7]
                record_type = line[7:9]
                data = line[8:-3]
                checksum = line[-3:]

                print(f"Byte Count: {byte_count}, Address: {address}, Type: {record_type}, Data: {data}, Checksum: {checksum}")

# Example usage
parse_hex("SCIM_SBL.hex")
'''
def parse_hex(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("S"):
                record_type = line[1] 
                byte_count = int(line[2:4], 16)
                address = line[4:8]
                data = line[8:-3]
                checksum = line[-3:]

                print(f"Byte Count: {byte_count}, Address: {address}, Type: {record_type}, Data: {data}, Checksum: {checksum}")

# Example usage
parse_hex("SCIM_SBL.hex")
