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
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from mainkv import mainkv
from synth import SynthLayout
from flash import FlashLayout
from testLayout import TestLayout
import os, sys
from kivy.resources import resource_add_path, resource_find

Builder.load_string(mainkv)

class NavScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        # Add widgets
        self.synth = SynthLayout(toFlash=self.toFlash)
        self.ids["mainlayout"].add_widget(self.synth)
        self.flash = FlashLayout()
        self.ids["flashlayout"].add_widget(self.flash)
        # For testing only
        self.test = TestLayout()
        self.ids["testlayout"].add_widget(self.test)

    def toFlash(self, fname):
        self.flash.ids["bitstream"].text = fname
        self.ids["screenManager"].current = "FlashScreen"

class WebFPGA_GUI(MDApp):
    def build(self):
        return NavScreen()


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    WebFPGA_GUI().run()
