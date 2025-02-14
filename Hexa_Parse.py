def parse_hex(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(":"):
                byte_count = int(line[1:3], 16)
                address = line[3:7]
                record_type = line[7:9]
                data = line[9:-2]
                checksum = line[-2:]

                print(f"Byte Count: {byte_count}, Address: {address}, Type: {record_type}, Data: {data}, Checksum: {checksum}")

# Example usage
parse_hex("example.hex")
