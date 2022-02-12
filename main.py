import xml.etree.ElementTree as ET

tree = ET.parse('dataset.xml')
root = tree.getroot()
print(root) 

for verbdatenbank in root:
    for verben_gruppe in verbdatenbank:
        print(verben_gruppe)