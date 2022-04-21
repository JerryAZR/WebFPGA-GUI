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

mainkv = """
<NavScreen>:
    MDNavigationLayout:
        ScreenManager:
            id: screenManager
            Screen:
                id: mainScreen
                name: "MainScreen"
                MDGridLayout:
                    cols: 1
                    id: mainlayout
                    MDToolbar:
                        title: "Synthesis Verilog Files"
                        left_action_items: [["menu", lambda x: navDrawer.set_state("open")]]

            Screen:
                id: flashScreen
                name: "FlashScreen"
                MDGridLayout:
                    cols: 1
                    id: flashlayout
                    MDToolbar:
                        title: "Flash Bitstream"
                        left_action_items: [["menu", lambda x: navDrawer.set_state("open")]]

            Screen:
                id: infoScreen
                name: "InfoScreen"
                MDGridLayout:
                    cols: 1
                    id: infolayout
                    MDToolbar:
                        title: "About WebFPGA-GUI"
                        left_action_items: [["menu", lambda x: navDrawer.set_state("open")]]
                    
            Screen:
                id: testScreen
                name: "TestScreen"
                MDGridLayout:
                    cols: 1
                    id: testlayout
                    MDToolbar:
                        title: "Test Page"
                        left_action_items: [["menu", lambda x: navDrawer.set_state("open")]]

        MDNavigationDrawer:
            id: navDrawer
            MDGridLayout:
                cols: 1
                ScrollView:
                    MDList:
                        OneLineIconListItem:
                            id: selectMain
                            text: "Synthesis"
                            on_release:
                                navDrawer.set_state("close");
                                screenManager.current = "MainScreen"
                            IconLeftWidget:
                                icon: "memory"
                        OneLineIconListItem:
                            id: selectFlash
                            text: "Flash"
                            on_release: 
                                navDrawer.set_state("close");
                                screenManager.current = "FlashScreen"
                            IconLeftWidget:
                                icon: "usb-port"
                        OneLineIconListItem:
                            id: selectInfo
                            text: "About"
                            on_release: 
                                navDrawer.set_state("close");
                                screenManager.current = "InfoScreen"
                            IconLeftWidget:
                                icon: "information"
                        # OneLineIconListItem:
                        #     id: selectTest
                        #     text: "Test Screen"
                        #     on_release:
                        #         navDrawer.set_state("close");
                        #         screenManager.current = "TestScreen"
                        #     IconLeftWidget:
                        #         icon: "wrench"
"""
