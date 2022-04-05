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
                            id: selectTest
                            text: "Test Screen"
                            on_release:
                                navDrawer.set_state("close");
                                screenManager.current = "TestScreen"
                            IconLeftWidget:
                                icon: "menu"
"""
