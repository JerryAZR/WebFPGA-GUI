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

synthkv = """
<SynthLayout>
    cols: 1
    padding: [0, 0, 0, 0]   # [left, top, right, bottom]
    active_color: app.theme_cls.primary_color
    btnFontSize: 20
    MDGridLayout:
        cols: 2
        adaptive_height: True
        MDGridLayout:
            rows: 1
            adaptive_height: True
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "center"
                MDGridLayout:
                    rows: 1
                    adaptive_size: True
                    spacing: 16
                    MDFillRoundFlatIconButton:
                        id: addFileBtn
                        icon: "book-plus"
                        text: "Add file"
                        font_size: root.btnFontSize
                        md_bg_color: root.active_color
                    MDFillRoundFlatIconButton:
                        id: rmAllFilesBtn
                        icon: "book-remove-multiple"
                        text: "Remove all"
                        font_size: root.btnFontSize
                        md_bg_color: root.active_color
        MDGridLayout:
            rows: 1
            adaptive_height: True
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "center"
                MDGridLayout:
                    rows: 1
                    adaptive_size: True
                    spacing: 16
                    MDFillRoundFlatIconButton:
                        id: synthBtn
                        icon: "memory"
                        text: "Synthesis"
                        font_size: root.btnFontSize
                        md_bg_color: (100, 100, 100) if synthBtn.disabled else root.active_color
                        disabled: synthSpinner.active
                    MDGridLayout:
                        rows: 1
                        adaptive_size: True
                        spacing: 4
                        MDCheckbox:
                            id: useCache
                            size_hint: (None, None)
                            size: (useCacheLabel.font_size, useCacheLabel.font_size)
                            active: True
                        MDTextButton:
                            id: useCacheLabel
                            text: "use cache"
                    MDSpinner:
                        id: synthSpinner
                        size_hint: (None, None)
                        size: (48, 48)
                        active: False

    ScrollView:
        MDGridLayout:
            cols: 1
            id: fileListLayout
            adaptive_height: True

<FileEntry>:
    rows: 1
    adaptive_height: True
    padding: [24, 0]    # [horizontal, vertical]
    MDLabel:
        id: fileNameLabel
        font_name: app.font_name
    MDIconButton:
        id: deleteEntryBtn
        icon: "book-remove"
        root: root      # Make root available in python code

"""