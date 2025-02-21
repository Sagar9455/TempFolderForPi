import xml.etree.ElementTree as ET

tree=ET.parse('details.xml')

root=tree.getroot()

print(root.tag)
for child in root:
    print(child[0].text)
