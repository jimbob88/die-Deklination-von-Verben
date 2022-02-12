import xml.etree.ElementTree as ET
from asciimatics.screen import ManagedScreen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
import time

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
@ManagedScreen
def demo(screen=None):
    screen.print_at('Hello world!', 0, 0)
    screen.print_at(u' Call me!', 10, 10, screen.COLOUR_GREEN, screen.A_BOLD)
    screen.refresh()
    time.sleep(10)
demo()