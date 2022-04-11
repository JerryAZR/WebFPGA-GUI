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

flashkv = """
<FlashLayout>:
    cols: 1
    adaptive_height: True
    spacing: 16
    padding: 16
    active_color: app.theme_cls.primary_color
    btnFontSize: 20
    MDGridLayout:
        rows: 1
        adaptive_height: True
        MDIcon:
            icon: "file-star"
            size_hint: (None, None)
            size: (sizeref.font_size * 2, sizeref.font_size)
        MDLabel:
            id: sizeref
            text: "Bitstream file to use:"
            font_size: root.btnFontSize
    MDTextField:
        id: bitstream
        text: "bitstream.bin"
        font_name: app.font_name
    MDGridLayout:
        rows: 1
        adaptive_height: True
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            MDFillRoundFlatIconButton:
                id: fileBtn
                icon: "book-plus"
                text: "Select bitstream file"
                font_size: root.btnFontSize
                md_bg_color: root.active_color
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            MDFillRoundFlatIconButton:
                id: flashBtn
                icon: "usb-port"
                text: "Program FPGA"
                font_size: root.btnFontSize
                disabled: False
                md_bg_color: (100, 100, 100) if flashBtn.disabled else root.active_color

"""