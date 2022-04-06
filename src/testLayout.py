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
from testkv import testkv
from popups import SynthPopup, SynthResultPopup

Builder.load_string(testkv)

class TestLayout(MDGridLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids["synthPopupTestBtn"].bind(on_release=self.synthPopupTest)
        self.ids["synthSuccessTestBtn"].bind(on_release=self.synthSuccessTest)
        self.ids["synthFailTestBtn"].bind(on_release=self.synthFailTest)

    def synthPopupTest(self, *args):
        popup = SynthPopup()
        popup.open()

    def synthSuccessTest(self, *args):
        popup = SynthResultPopup(warnings=[
            "WARNING 1",
            "WARNING 2"
        ])
        popup.ids["filepath"].text = f"""
        Bitstream save location:
        {"Very long file path to mess with the pop up window"}
        """
        popup.open()

    def synthFailTest(self, *args):
        popup = SynthResultPopup(success=False, warnings=[
            "ERROR 1",
            "WARNING 1",
            "WARNING 2"
        ])
        popup.ids["filepath"].text = """
This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.
        """
        popup.open()
        
