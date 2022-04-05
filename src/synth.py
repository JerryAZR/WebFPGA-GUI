from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from easygui import fileopenbox, filesavebox

import asyncio
from GUISynthesis import Synthesize

from synthkv import synthkv

Builder.load_string(synthkv)

class SynthLayout(MDGridLayout):
    btnFontSize = 20
    saveBin = "Where would you like to save the bitstream?"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids["addFileBtn"].font_size = self.btnFontSize
        self.ids["rmAllFilesBtn"].font_size = self.btnFontSize
        self.ids["synthBtn"].font_size = self.btnFontSize

        self.ids["addFileBtn"].bind(on_release=self.file_select)
        self.ids["rmAllFilesBtn"].bind(on_release=self.file_clear)
        self.ids["synthBtn"].bind(on_release=self.synth_start)
        self.ids["useCacheLabel"].bind(on_release=self.toggle_cache)

        self.verilogList = []

    def toggle_cache(self, *args):
        self.ids["useCache"].active = not self.ids["useCache"].active

    def file_select(self, *args):
        fnames = fileopenbox(multiple=True, default="*.v")
        if (fnames is None):
            return
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
            return
        # open output file
        bitstream = filesavebox(msg=self.saveBin, default="bitstream.bin")
        if (bitstream is None):
            return
        if (not bitstream.endswith(".bin")):
            bitstream += ".bin"
        outfile = open(bitstream, "wb")
        
        # open the input files
        infiles = []
        for v in self.verilogList:
            infiles.append(open(v, "r"))

        # check "--no-cache" option
        no_cache = not self.ids["useCache"].active

        # Start spinner and disable synthesis button
        self.ids["synthSpinner"].active = True

        self.success = [False]

        asyncio.run(Synthesize(
            input_verilog=infiles,
            output_bitstream=outfile,
            no_cache=no_cache,
            success=self.success)
        )

        # close used files
        for v in infiles:
            v.close()
        outfile.close()

        # stop spinner and enable synthesis button
        self.ids["synthSpinner"].active = False

        if (self.success[0]):
            print("Synthesis complete")
        else:
            print("Synthesis failed")

class FileEntry(MDGridLayout):
    def __init__(self, name, on_delete, **kw):
        super().__init__(**kw)
        # self.on_delete = on_delete
        self.ids["fileNameLabel"].text = name
        self.ids["deleteEntryBtn"].bind(on_release=on_delete)


