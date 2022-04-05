from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from popups import SynthPopup
from easygui import fileopenbox, exceptionbox, msgbox

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
        self.ids["flashBtn"].disabled = True
        fname = self.ids["bitstream"].text
        # TODO: move this to a separate thread and add a progress bar
        try:
            with open(fname, "rb") as bitstream:
                Flash(bitstream.read())
            msgbox(msg="FPGA programmed")
        except:
            exceptionbox()
        self.ids["flashBtn"].disabled = False
