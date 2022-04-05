from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from popupkv import *

Builder.load_string(synthPopupkv)

class SynthPopup(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.state = 0
        self.ids["taskList"].add_widget(
            ProgressEntry(text="Initialization", state=1)
        )
        for i in range(6):
            self.ids["taskList"].add_widget(
                ProgressEntry(text=f"Phase {i+1}", state=0)
            )

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
