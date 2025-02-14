def parse_mot(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            record_type = line[:2]  # First two characters (e.g., S0, S1, etc.)
            byte_count = int(line[2:4], 16)  # Number of bytes
            address = line[4:8] if record_type in ["S1", "S9"] else line[4:10]  # Address
            data = line[8:-2]  # Data bytes
            checksum = line[-2:]  # Last two characters

            print(f"Type: {record_type}, Address: {address}, Data: {data}, Checksum: {checksum}")

# Example usage
parse_mot("example.mot")
