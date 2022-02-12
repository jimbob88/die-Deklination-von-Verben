import xml.etree.ElementTree as ET

tree = ET.parse('dataset.xml')
root = tree.getroot()
print(root) 

for verben_gruppe in root:
    print(verben_gruppe.attrib)
    for verb in verben_gruppe:
        print(verb)