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

synthPopupkv = """
<SynthPopup>:
    auto_dismiss: False
    title: "Synthesis In Progress"
    size_hint: (0.8, 0.8)
    MDGridLayout:
        cols:1
        MDGridLayout:
            id: taskList
            cols:1
            padding: 16
            spacing: 16
        MDGridLayout:
            rows:1
            adaptive_height: True
            Widget: # placeholder
            Button:
                id: stopBtn
                size_hint_y: None
                height: self.font_size * 3
                text: "Stop synthesis"
                on_release: root.dismiss()

<ProgressEntry@MDGridLayout>:
    rows: 1
    adaptive_height: True
    spacing: 4
    text: "Progress text"
    state: 0
    state_icons: ["clock-outline", "play", "check"]
    Label:
        id: label
        halign: 'left'
        valign: 'middle'
        text: root.text
    MDIcon:
        icon: root.state_icons[root.state]
        size_hint: (None, None)
        size: (label.font_size * 2, label.font_size)
    MDSpinner:
        active: root.state == 1
        size_hint: (None, None)
        size: (label.font_size, label.font_size)

"""

synthSuccessPopupkv = """
<SynthSuccessPopup@Popup>:
    title: "Synthesis Completed!"
    size_hint_x: 0.8
    size_hint_y: None
    height: container.height * 1.8
    MDGridLayout:
        id: container
        cols:1
        adaptive_height: True
        Label:
            id: filepath
        MDGridLayout:
            rows: 1
            Button:
                text: "Close"
                on_release: root.dismiss()
            Button:
                id: warnBtn
                text: "Check warnings"
            Button:
                id: flashBtn
                text: "Program FPGA"
                on_release: root.dismiss()

"""
