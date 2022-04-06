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
from popups import FlashPopup
from easygui import fileopenbox
from flashkv import flashkv
from GUIFlash import startFlashThread

Builder.load_string(flashkv)

class FlashLayout(MDGridLayout):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.ids["fileBtn"].bind(on_release=self.file_select)
        self.ids["flashBtn"].bind(on_release=self.program_fpga)

    def file_select(self, *args):
        fname = fileopenbox(multiple=False, default="*.bin")
        if (fname is None):
            return
        self.ids["bitstream"].text = fname

    def program_fpga(self, *args):
        self.ids["flashBtn"].disabled = True
        fname = self.ids["bitstream"].text

        progress = FlashPopup()
        progress.open()
        startFlashThread(fname, progress, self.program_done)

    def program_done(self, *args):
        self.ids["flashBtn"].disabled = False
