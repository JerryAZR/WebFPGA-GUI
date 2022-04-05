from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from popupkv import *
from easygui import textbox

Builder.load_string(synthPopupkv)

class SynthPopup(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.state = 0
        self.keywords = [
            "found the top-level module",
            "Synthesis to EDIF is good.",
            "Placer is good.",
            "Router is good.",
            "Netlister is good.",
            "Bit File Generation is good.",
            "purging build directory..."
        ]
        self.ids["taskList"].add_widget(ProgressEntry(text="Analysis", state=1))
        self.ids["taskList"].add_widget(ProgressEntry(text="Synthesis", state=0))
        self.ids["taskList"].add_widget(ProgressEntry(text="Placement", state=0))
        self.ids["taskList"].add_widget(ProgressEntry(text="Routing", state=0))
        self.ids["taskList"].add_widget(ProgressEntry(text="Netlist generation", state=0))
        self.ids["taskList"].add_widget(ProgressEntry(text="Bitstream generation", state=0))
        self.ids["taskList"].add_widget(ProgressEntry(text="Cleanup", state=0))

    def forward(self, *args):
        # reverse the list to get the right order
        children = self.ids["taskList"].children[::-1]
        # mark current task as completed
        children[self.state].state = 2
        # mark the next task (if available) as started
        self.state += 1
        if (self.state < len(children)):
            children[self.state].state = 1

class ProgressEntry(MDGridLayout):
    def __init__(self, text="Progress", state=0, **kw):
        super().__init__(**kw)
        self.text = text
        self.state = state

Builder.load_string(synthSuccessPopupkv)

class SynthSuccessPopup(Popup):
    def __init__(self, warnings=[], **kw):
        super().__init__(**kw)
        self.warnings = warnings
        self.ids["warnBtn"].bind(on_release=self.show_warnings)

    def show_warnings(self, *args):
        textbox(
            title="Warnings",
            text="\n".join(self.warnings)
        )
