import xml.etree.ElementTree as ET

def parse_cdd(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    services = {}
    for service in root.find('Services'):
        service_id = service.attrib['id']
        service_name = service.attrib['name']
        subservices = {}
        for subservice in service.findall('SubServices/SubService'):
            sub_id = subservice.attrib['id']
            sub_name = subservice.attrib['name']
            subservices[sub_name] = sub_id
        services[service_name] = {'id': service_id, 'subservices': subservices}

    return services


def main():
    file_path = 'path/to/your/file.cdd'  # Change to your actual path
    uds_data = parse_cdd(file_path)

    print("Available Services:")
    for service in uds_data:
        print(service)

    service_name = input("Select a Service: ")
    if service_name in uds_data:
        print("Selected Service ID:", uds_data[service_name]['id'])
        if uds_data[service_name]['subservices']:
            print("Available SubServices:")
            for sub in uds_data[service_name]['subservices']:
                print(sub)

            sub_name = input("Select a SubService: ")
            if sub_name in uds_data[service_name]['subservices']:
                print("Selected SubService ID:", uds_data[service_name]['subservices'][sub_name])
                print("For Raspberry Pi: {} {}".format(uds_data[service_name]['id'], uds_data[service_name]['subservices'][sub_name]))
            else:
                print("SubService not found.")
        else:
            print("No SubServices available.")
    else:
        print("Service not found.")


if __name__ == "__main__":
    main()
