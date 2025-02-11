import xml.etree.ElementTree as ET

def parse_uds_config(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    uds_data = {
        "services": [],
        "dtcs": [],
        "nrcs": [],
        "responses": {"positive": [], "negative": []}
    }

    # Parse Services
    for service in root.find("Services"):
        service_data = {
            "id": service.get("id"),
            "name": service.get("name"),
            "sub_services": []
        }
        sub_services = service.find("SubServices")
        if sub_services is not None:
            for sub_service in sub_services:
                service_data["sub_services"].append({
                    "id": sub_service.get("id"),
                    "name": sub_service.get("name")
                })
        uds_data["services"].append(service_data)

    # Parse DTCs
    for dtc in root.find("DTCs"):
        uds_data["dtcs"].append({
            "id": dtc.get("id"),
            "description": dtc.get("description"),
            "severity": dtc.get("severity")
        })

    # Parse NRCs
    for nrc in root.find("NRCs"):
        uds_data["nrcs"].append({
            "id": nrc.get("id"),
            "description": nrc.get("description")
        })

    # Parse Responses
    responses = root.find("Responses")
    for pos_resp in responses.find("Positive"):
        uds_data["responses"]["positive"].append({
            "id": pos_resp.get("id"),
            "description": pos_resp.get("description")
        })

    for neg_resp in responses.find("Negative"):
        uds_data["responses"]["negative"].append({
            "id": neg_resp.get("id"),
            "description": neg_resp.get("description")
        })

    return uds_data

# Example usage
xml_file = "uds_config.xml"  # Replace with actual file path
uds_data = parse_uds_config(xml_file)

# Print parsed data
import json
print(json.dumps(uds_data, indent=4))
