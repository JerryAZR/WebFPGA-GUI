from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from testkv import testkv
from popups import SynthPopup, SynthSuccessPopup

Builder.load_string(testkv)

class TestLayout(MDGridLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids["synthPopupTestBtn"].bind(on_release=self.synthPopupTest)
        self.ids["synthSuccessTestBtn"].bind(on_release=self.synthSuccessTest)

    def synthPopupTest(self, *args):
        popup = SynthPopup()
        popup.open()

    def synthSuccessTest(self, *args):
        popup = SynthSuccessPopup(warnings=[
            "WARNING 1",
            "WARNING 2"
        ])
        popup.ids["filepath"].text = f"""
        Bitstream save location:
        {"Very long file path to mess with the pop up window"}
        """
        popup.open()
