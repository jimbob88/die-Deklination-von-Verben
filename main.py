import xml.etree.ElementTree as ET
from asciimatics.screen import ManagedScreen, Screen, KeyboardEvent
from asciimatics.widgets import Frame, Text, TextBox, Layout, Label, Button, PopUpDialog, Widget, ListBox, Divider
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
        print(verben_buch.keys())
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            list(zip(verben_buch.keys(), verben_buch.keys())),
            name="contacts",
            add_scroll_bar=True)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        self.fix()

        self._learn_button = Button("Learn", self._learn)
        # self._delete_button = Button("Delete", self._delete)
        # layout2 = Layout([1, 1, 1, 1])
        # self.add_layout(layout2)
        # layout2.add_widget(Button("Add", self._add), 0)
        # layout2.add_widget(self._edit_button, 1)
        # layout2.add_widget(self._delete_button, 2)
        # layout2.add_widget(Button("Quit", self._quit), 3)
        # self.fix()
        # self._on_pick()
    
    def _on_pick(self):
        self._learn_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _learn(self):
        print("learn")

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["contacts"]
        raise NextScene("Edit Contact")

    def _delete(self):
        self.save()
        self._model.delete_contact(self.data["contacts"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        c = event.key_code
        # Stop on ctrl+q or ctrl+x
        if c in (17, 24):
            raise StopApplication("User terminated app")

def demo(screen, scene):
    scenes = [
        Scene([GroupFrame(screen)], -1, name="Main"),
        # Scene([ContactView(screen)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True, unhandled_input=global_shortcuts)


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene