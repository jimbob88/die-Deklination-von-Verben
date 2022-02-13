import xml.etree.ElementTree as ET
import urwid
import urwidtrees
from urwidtrees.tree import SimpleTree
from urwidtrees.widgets import TreeBox
from urwidtrees.decoration import ArrowTree
import os


tree = ET.parse("dataset.xml")
root = tree.getroot()
print(root)

verben_buch = {}

for verben_gruppe in root:
    print(verben_gruppe.attrib["gruppe"])
    verben_buch[verben_gruppe.attrib["gruppe"]] = {}
    for verb in verben_gruppe:
        verben_buch[verben_gruppe.attrib["gruppe"]][verb.attrib["infinitiv"]] = verb
        print(verb)

print(verben_buch)

palette = [
    ("body", "black", "light gray"),
    ("focus", "light gray", "dark blue", "standout"),
    ("bars", "dark blue", "light gray", ""),
    ("arrowtip", "light blue", "light gray", ""),
    ("connectors", "light red", "light gray", ""),
]

# We use selectable Text widgets for our example..


class FocusableText(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt):
        t = urwid.Text(txt)
        w = urwid.AttrMap(t, "body", "focus")
        urwid.WidgetWrap.__init__(self, w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


def unhandled_input(k):
    # exit on q
    if k in ["q", "Q"]:
        raise urwid.ExitMainLoop()
    if k in ["l", "L"]:
        views[0].selected = views[0].treebox._walker.get_focus()
        print()


class select_view(object):
    def __init__(self):
        self.selected = False

    def build(self):
        stree = SimpleTree(
            [
                [
                    FocusableText("All"),
                    [
                        [
                            FocusableText(k),
                            [[FocusableText(verb), None] for verb in v.keys()],
                        ]
                        for k, v in verben_buch.items()
                    ],
                ]
            ]
        )

        # put the tree into a treebox
        self.treebox = TreeBox(ArrowTree(stree))

        # add some decoration
        rootwidget = urwid.AttrMap(self.treebox, "body")
        # add a text footer
        footer = urwid.AttrMap(urwid.Text("Q to quit, L to learn"), "focus")
        return urwid.Frame(rootwidget, footer=footer)


print(verben_buch)
if __name__ == "__main__":
    # get example tree
    # stree = construct_example_tree()
    # stree = SimpleTree([[FocusableText(k), [FocusableText("generic")]] for k, v in verben_buch.items()])
    
    # enclose all in a frame

    views = [
            select_view()
        ]

    initial_view = views[0].build()
    loop = urwid.MainLoop(
        initial_view, palette, unhandled_input=unhandled_input
    )
    loop.run()
