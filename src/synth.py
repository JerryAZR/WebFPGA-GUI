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

import os
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.toast import toast
from popups import SynthPopup, SynthResultPopup
from easygui import fileopenbox, filesavebox

import asyncio
from GUISynthesis import startSynthThread

from synthkv import synthkv

Builder.load_string(synthkv)

class Collection():
    def __init__(self, onComplete, onKeyword, keywords=[]):
        self.run = True
        self.success = False
        self.done = False
        self.onComplete = onComplete
        self.errors = []
        self.warnings = []
        self.keywords = keywords
        self.onKeyword = onKeyword

    def terminate(self, *args):
        self.run = False

class SynthLayout(MDGridLayout):
    saveBin = "Where would you like to save the bitstream?"

    def __init__(self, toFlash, **kw):
        super().__init__(**kw)

        self.ids["addFileBtn"].bind(on_release=self.file_select)
        self.ids["rmAllFilesBtn"].bind(on_release=self.file_clear)
        self.ids["synthBtn"].bind(on_release=self.synth_start)
        self.ids["useCacheLabel"].bind(on_release=self.toggle_cache)

        self.verilogList = []
        self.synthPopup = None
        self.bitstream = "./bitstream.bin"
        self.toFlash = toFlash
        self.verilogDir = "./"

    def toggle_cache(self, *args):
        self.ids["useCache"].active = not self.ids["useCache"].active

    def file_select(self, *args):
        # Open file dialog box at previous location
        defaultPath = os.path.join(self.verilogDir, "*.v")
        fnames = fileopenbox(multiple=True, default=defaultPath)
        if (fnames is None):
            return
        # update default verilog path
        self.verilogDir = os.path.dirname(fnames[0])
        for fname in fnames:
            if (fname not in self.verilogList):
                self.verilogList.append(fname)
                newEntry = FileEntry(fname, self.file_delete)
                self.ids["fileListLayout"].add_widget(newEntry)

    def file_clear(self, *args):
        self.ids["fileListLayout"].clear_widgets()
        self.verilogList = []

    def file_delete(self, instance):
        entry = instance.root
        fname = instance.root.ids["fileNameLabel"].text
        self.verilogList.remove(fname)
        self.ids["fileListLayout"].remove_widget(entry)

    def synth_start(self, *args):
        # check if file list is empty
        if (len(self.verilogList) == 0):
            toast("Please add at lease one Verilog file.")
            return
        # open output file
        tmp = filesavebox(msg=self.saveBin, default=self.bitstream)
        if (tmp is None):
            return
        # Update default bitstream path if not None
        self.bitstream = tmp
        if (not self.bitstream.endswith(".bin")):
            self.bitstream += ".bin"

        # check "--no-cache" option
        no_cache = not self.ids["useCache"].active

        # Start spinner and disable synthesis button
        self.ids["synthSpinner"].active = True

        self.synthPopup = SynthPopup()

        self.colle = Collection(
            onComplete=self.synth_cleanup,
            keywords=self.synthPopup.keywords,
            onKeyword=self.synthPopup.forward
        )

        # Bind the stop function
        self.synthPopup.ids["stopBtn"].bind(on_release=self.colle.terminate)
        self.synthPopup.open()

        startSynthThread(
            input_verilog=self.verilogList,
            output_bitstream=self.bitstream,
            no_cache=no_cache,
            collection=self.colle
        )

    def synth_cleanup(self, *args):
        # stop spinner and enable synthesis button
        self.ids["synthSpinner"].active = False
        self.synthPopup.dismiss()
        self.synthPopup = None

        popup = SynthResultPopup(
            success=self.colle.success,
            warnings=(self.colle.errors + self.colle.warnings)
        )

        if (self.colle.success):
            popup.ids["flashBtn"].bind(on_release=self.toFlashWrapper)
            popup.ids["filepath"].text = f"""
            Bitstream save location:
            {self.bitstream}
            """
        else:
            if (len(self.colle.errors) > 0):
                popup.ids["filepath"].text = self.colle.errors[0]
        popup.open()

    def toFlashWrapper(self, *args):
        self.toFlash(self.bitstream)

class FileEntry(MDGridLayout):
    def __init__(self, name, on_delete, **kw):
        super().__init__(**kw)
        # self.on_delete = on_delete
        self.ids["fileNameLabel"].text = name
        self.ids["deleteEntryBtn"].bind(on_release=on_delete)


