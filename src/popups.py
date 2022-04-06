"""
This file is part of the WebFPGA-GUI program
(https://github.com/JerryAZR/WebFPGA-GUI).

Copyright (c) 2022, Zerui An <anzerui@126.com / jerryazr@gmail.com>.

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.

The WebFPGA-GUI program is based on the WebFPGA CLI tool developed
by the WebFPGA Team (https://github.com/webfpga/cli). The Copyright
of the original program belongs to Auburn Ventures, LLC and is
covered by the MIT License (https://opensource.org/licenses/MIT).
"""

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

Builder.load_string(synthResultPopupkv)

class SynthResultPopup(Popup):
    def __init__(self, success=True, warnings=[], **kw):
        super().__init__(**kw)
        self.title = "Synthesis Completed!" if success else "Synthesis Failed"
        self.warnings = warnings
        self.ids["warnBtn"].bind(on_release=self.show_warnings)
        self.ids["flashBtn"].disabled = not success

    def show_warnings(self, *args):
        textbox(
            title="Warnings",
            text="\n".join(self.warnings)
        )

Builder.load_string(flashPopupkv)

class FlashPopup(Popup):
    pass
