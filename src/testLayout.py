from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from testkv import testkv
from popups import SynthPopup

Builder.load_string(testkv)

class TestLayout(MDGridLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids["synthPopupTestBtn"].bind(on_release=self.synthPopupTest)

    def synthPopupTest(self, *args):
        popup = SynthPopup()
        popup.open()
