from lxml import etree as ET
import urwid
import urwidtrees
from urwidtrees.tree import SimpleTree
from urwidtrees.widgets import TreeBox
from urwidtrees.decoration import ArrowTree
import os
from collections.abc import Iterable

tree = ET.parse("dataset.xml")
root = tree.getroot()

SHORTHAND = {"h": "haben", "s": "sein"}

verben_buch = {}

for verben_gruppe in root:
    verben_buch[verben_gruppe.attrib["gruppe"]] = {}
    for verb in verben_gruppe:
        verben_buch[verben_gruppe.attrib["gruppe"]][verb.attrib["infinitiv"]] = [
            tense for tense in verb
        ]

palette = [
    ("body", "black", "light gray"),
    ("focus", "light gray", "dark blue", "standout"),
    ("bars", "dark blue", "light gray", ""),
    ("arrowtip", "light blue", "light gray", ""),
    ("connectors", "light red", "light gray", ""),
]

# We use selectable Text widgets for our example..


def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


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
    elif k in ["l", "L"]:
        _, idx = initial_view.treebox._walker.get_focus()
        if len(idx) == 3:
            verb = initial_view.tree[1][idx[1]][1][idx[2]]
            loop.widget = learn_view().build(verb)
    elif k in ["v", "V"]:
        _, idx = initial_view.treebox._walker.get_focus()
        if len(idx) == 3:
            verb = initial_view.tree[1][idx[1]][1][idx[2]]
            loop.widget = verb_view().build(verb)
    elif k in ["h", "H"]:
        loop.widget = select_view().build()


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

        self.treebox = TreeBox(ArrowTree(self.stree))
        rootwidget = urwid.AttrMap(self.treebox, "body")
        footer = urwid.AttrMap(urwid.Text("Q to quit, L to learn, V to view"), "focus")
        return urwid.Frame(rootwidget, footer=footer)


class verb_view(object):
    def __init__(self):
        pass

    def build(self, verb):

        blank = urwid.Divider()
        listbox_content = [
            [
                urwid.Text(tense.tag, align="center"),
                [
                    [urwid.Text(f"{declension.tag} - {declension.attrib['verb']}")]
                    for declension in tense
                ],
            ]
            if tense.tag != "perfekt"
            else [
                urwid.Text(tense.tag, align="center"),
                [
                    urwid.Text(
                        f"{SHORTHAND[tense.attrib['hs']]} + {tense.attrib['partzip']}"
                    )
                ],
            ]
            for tense in verb[1][0]
        ]
        listbox_content = list(flatten((listbox_content)))
        print(listbox_content)
        header = urwid.AttrWrap(urwid.Text(verb[0]), "header")
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, "body"), header=header)
        return frame


class learn_view(object):
    def __init__(self):
        pass

    def build(self, verb):
        blank = urwid.Divider()
        self.listbox_content = [
            [
                urwid.Text(tense.tag, align="center"),
                [
                    urwid.Edit(f"{declension.tag}: ", align="left")
                    for declension in tense
                ],
            ]
            if tense.tag != "perfekt"
            else [
                urwid.Text(tense.tag, align="center"),
                [urwid.Edit(f"Formed with: "), urwid.Edit(f"Partzip: ")],
            ]
            for tense in verb[1][0]
        ]
        self.answers = list(
            flatten(
                [
                    [declension.attrib["verb"] for declension in tense]
                    if tense.tag != "perfekt"
                    else [SHORTHAND[tense.attrib["hs"]], tense.attrib["partzip"]]
                    for tense in verb[1][0]
                ]
            )
        )
        self.enter_button = urwid.Button("Enter")
        urwid.connect_signal(self.enter_button, "click", self.on_entry)
        self.listbox_content += [self.enter_button]
        self.listbox_content = list(flatten(self.listbox_content))
        header = urwid.AttrWrap(urwid.Text(verb[0]), "header")
        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, "body"), header=header)
        self.frame = frame
        return frame

    def on_entry(self, button):
        self.results = [
            entry.edit_text
            for entry in self.listbox_content
            if type(entry) == urwid.Edit
        ]
        print(self.results)
        print([ans.strip() for ans in self.answers])
        self._over = urwid.Overlay(
            self.answer_dialog(),
            self.frame,
            align="center",
            valign="middle",
            width=100,
            height=100,
        )
        loop.widget = self._over

    def answer_dialog(self):
        header_text = urwid.Text(("banner", "Help"), align="center")
        header = urwid.AttrMap(header_text, "banner")

        # Body
        # body_text = urwid.Text('Your Results!', align = 'center')
        print_results = [
            urwid.Text(
                f"I: {result} - A: {self.answers[idx]} = {result == self.answers[idx]}"
            )
            for idx, result in enumerate(self.results)
        ]
        body_filler = urwid.ListBox(urwid.SimpleListWalker(print_results))
        body_padding = urwid.Padding(body_filler, left=1, right=1)
        body = urwid.LineBox(body_padding)

        # Footer
        footer = urwid.Button("Okay", self.do)
        footer = urwid.AttrWrap(footer, "selectable", "focus")
        footer = urwid.GridFlow([footer], 8, 1, 1, "center")

        # Layout
        layout = urwid.Frame(body, header=header, footer=footer, focus_part="footer")

        return layout

    def do(self, thing):
        loop.widget = self.frame


print(verben_buch)
if __name__ == "__main__":

    initial_view = select_view()
    loop = urwid.MainLoop(initial_view.build(), palette, unhandled_input=unhandled_input)
    loop.run()
