import xml.etree.ElementTree as ET

# Load and parse the CDD file
def parse_cdd(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Extract important data (modify based on your CDD structure)
    for service in root.findall(".//DiagnosticService"):
        service_id = service.get("ServiceId")
        description = service.find("Description").text if service.find("Description") is not None else "No description"
        
        print(f"Service ID: {service_id}, Description: {description}")

# Example usage
parse_cdd("example.cdd")
