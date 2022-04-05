from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from popups import SynthPopup
from easygui import fileopenbox, exceptionbox

from flashkv import flashkv

from webfpga.Flash import Flash

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
        fname = self.ids["bitstream"].text
        try:
            with open(fname, "rb") as bitstream:
                Flash(bitstream.read())
            print("Done")
        except:
            exceptionbox()
