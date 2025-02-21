import xml.etree.ElementTree as ET

tree=ET.parse('namde.xml')
root=tree.getroot()


for DIAGINSTid in root.findall("_0CE73D98 "):
        service_id = service.get("ServiceId")
        description = service.find("Description").text if service.find("Description") is not None else "No description"
        
        print(f"Service ID: {service_id}, Description: {description}")



