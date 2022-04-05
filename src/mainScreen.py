from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from mainkv import mainkv
from synth import SynthLayout
from testLayout import TestLayout
import os, sys
from kivy.resources import resource_add_path, resource_find

Builder.load_string(mainkv)

class NavScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        # Add widgets
        self.synth = SynthLayout()
        self.ids["mainlayout"].add_widget(self.synth)
        # For testing only
        self.test = TestLayout()
        self.ids["testlayout"].add_widget(self.test)
        # bind menu events
        self.ids["selectMain"].bind(on_release=self.switch_main_screen)
        self.ids["selectTest"].bind(on_release=self.switch_test_screen)

    def switch_main_screen(self, *args):
        self.ids["navDrawer"].set_state("close")
        self.ids["screenManager"].current = "MainScreen"
    
    def switch_test_screen(self, *args):
        self.ids["navDrawer"].set_state("close")
        self.ids["screenManager"].current = "TestScreen"

class WebFPGA_GUI(MDApp):
    def build(self):
        return NavScreen()


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    WebFPGA_GUI().run()
