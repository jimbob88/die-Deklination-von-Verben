import xml.etree.ElementTree as ET
from asciimatics.screen import ManagedScreen, Screen
from asciimatics.widgets import Frame, Text, TextBox, Layout, Label, Button, PopUpDialog, Widget
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import time
import sys

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

class GroupFrame(Frame):
    def __init__(self, screen):
        super(GroupFrame, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Choose a verb group",
                                          reduce_cpu=True)


def demo(screen, scene):
    scenes = [
        Scene([GroupFrame(screen)], -1, name="Main"),
        # Scene([ContactView(screen)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene