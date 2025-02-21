import xml.etree.ElementTree as ET

tree=ET.parse('Ecu.cdd')

root=tree.getroot()

print(root.tag)

print(root[0][1][0][0][0].text)
for child in root[0][1]:
    print(child[0].text)
