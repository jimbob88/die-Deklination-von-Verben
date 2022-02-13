import xml.etree.ElementTree as ET
from picotui.screen import Screen
import picotui.widgets as pw
import picotui.defs as pdefs

tree = ET.parse('dataset.xml')
root = tree.getroot()
print(root) 

verben_buch = {}

for verben_gruppe in root:
    print(verben_gruppe.attrib['gruppe'])
    verben_buch[verben_gruppe.attrib['gruppe']] = {}
    for verb in verben_gruppe:
        verben_buch[verben_gruppe.attrib['gruppe']][verb.attrib['infinitiv']] = verb
        print(verb)

print(verben_buch)

s = Screen()

s.init_tty()
s.enable_mouse()
s.attr_color(pdefs.C_WHITE, pdefs.C_BLUE)
s.cls()
s.attr_reset()
d = pw.Dialog(5, 5, 20, 12)