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
        if not views[0].selected:
            views[0].selected = views[0].treebox._walker.get_focus()
    if k in ["v", "V"]:
        urwid.ExitMainLoop()
        focus_widget, idx = views[0].treebox._walker.get_focus()
        # print(views[0].tree[idx[0]+1][idx[1]+1][idx[2]])
        if len(idx) == 3:
            verb = views[0].tree[1][idx[1]][1][idx[2]]
        loop.widget = verb_view().build(verb)


class select_view(object):
    def __init__(self):
        self.selected = False

    def build(self):
        self.tree = [
            "All",
            [
                [
                    k,
                    [[verb, data] for verb, data in v.items()],
                ]
                for k, v in verben_buch.items()
            ],
        ]

        self.stree = SimpleTree(
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
        self.treebox = TreeBox(ArrowTree(self.stree))

        # add some decoration
        rootwidget = urwid.AttrMap(self.treebox, "body")
        # add a text footer
        footer = urwid.AttrMap(urwid.Text("Q to quit, L to learn"), "focus")
        return urwid.Frame(rootwidget, footer=footer)


class verb_view(object):
    def __init__(self):
        pass

    def build(self, verb):
        title = urwid.Text(verb[0])
        body = urwid.Text("Hello")
        body = urwid.Pile([title, body])
        fill = urwid.Filler(body)
        return fill


print(verben_buch)
if __name__ == "__main__":
    views = [select_view()]

    initial_view = views[0].build()
    loop = urwid.MainLoop(initial_view, palette, unhandled_input=unhandled_input)
    loop.run()
