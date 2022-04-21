"""
This program is a non-official GUI wrapper of the WebFPGA command line utility. The Source code of this program is available on GitHub: [ref=https://github.com/JerryAZR/WebFPGA-GUI][color=0000ff]https://github.com/JerryAZR/WebFPGA-GUI[/color][/ref].

Copyright (c) 2022, Zerui An <anzerui@126.com / jerryazr@gmail.com>.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [ref=http://www.gnu.org/licenses][color=0000ff]http://www.gnu.org/licenses[/color][/ref].

The WebFPGA-GUI program is based on the WebFPGA CLI tool developed by the WebFPGA Team ([ref=https://github.com/webfpga/cli][color=0000ff]https://github.com/webfpga/cli[/color][/ref]). The Copyright of the original program belongs to Auburn Ventures, LLC and is covered by the MIT License ([ref=https://opensource.org/licenses/MIT][color=0000ff]https://opensource.org/licenses/MIT[/color][/ref]).
"""

from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
import webbrowser

infokv = """
<InfoLayout@MDGridLayout>:
    cols: 1
    padding: 16
    ScrollView:
        MDLabel:
            id: infoLabel
            markup: True
            size_hint_y: None
            height: self.texture_size[1]
"""

Builder.load_string(infokv)

class InfoLayout(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids["infoLabel"].text = __doc__
        self.ids["infoLabel"].bind(on_ref_press=self.open_link)

    def open_link(self, instance, link):
        webbrowser.open(link,2) # Open in a new tab
