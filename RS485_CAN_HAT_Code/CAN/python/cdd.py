import xml.etree.ElementTree as ET
#parse XML into Element Tree (To make the contents of .cdd file into a structure)
tree=ET.parse('ECU.cdd')
root = tree.getroot()

print(root.tag)
