from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from popups import SynthPopup, SynthSuccessPopup
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
    btnFontSize = 20
    saveBin = "Where would you like to save the bitstream?"

    def __init__(self, toFlash, **kw):
        super().__init__(**kw)
        self.ids["addFileBtn"].font_size = self.btnFontSize
        self.ids["rmAllFilesBtn"].font_size = self.btnFontSize
        self.ids["synthBtn"].font_size = self.btnFontSize

        self.ids["addFileBtn"].bind(on_release=self.file_select)
        self.ids["rmAllFilesBtn"].bind(on_release=self.file_clear)
        self.ids["synthBtn"].bind(on_release=self.synth_start)
        self.ids["useCacheLabel"].bind(on_release=self.toggle_cache)

        self.verilogList = []
        self.synthPopup = None
        self.bitstream = ""
        self.toFlash = toFlash

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
        self.bitstream = filesavebox(msg=self.saveBin, default="bitstream.bin")
        if (self.bitstream is None):
            return
        if (not self.bitstream.endswith(".bin")):
            self.bitstream += ".bin"

        # check "--no-cache" option
        no_cache = not self.ids["useCache"].active

        # Start spinner and disable synthesis button
        self.ids["synthSpinner"].active = True

        self.synthPopup = SynthPopup()

        collection = Collection(
            onComplete=self.synth_cleanup,
            keywords=self.synthPopup.keywords,
            onKeyword=self.synthPopup.forward
        )

        # Bind the stop function
        self.synthPopup.ids["stopBtn"].bind(on_release=collection.terminate)
        self.synthPopup.open()

        startSynthThread(
            input_verilog=self.verilogList,
            output_bitstream=self.bitstream,
            no_cache=no_cache,
            collection=collection
        )

    def synth_cleanup(self, collection):
        # stop spinner and enable synthesis button
        self.ids["synthSpinner"].active = False
        self.synthPopup.dismiss()
        self.synthPopup = None

        if (collection.success):
            popup = SynthSuccessPopup()
            popup.ids["flashBtn"].bind(on_release=self.toFlashWrapper)
            popup.open()
        else:
            print("Synthesis failed")
            print("Error messages:")
            for msg in collection.errors:
                print(msg)

    def toFlashWrapper(self, *args):
        self.toFlash(self.bitstream)

class FileEntry(MDGridLayout):
    def __init__(self, name, on_delete, **kw):
        super().__init__(**kw)
        # self.on_delete = on_delete
        self.ids["fileNameLabel"].text = name
        self.ids["deleteEntryBtn"].bind(on_release=on_delete)


