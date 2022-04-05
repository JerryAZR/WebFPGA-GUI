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
                        id: mainTopBar
                        title: "Main Page"
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
                            text: "Main Screen"
                            IconLeftWidget:
                                icon: "memory"
                        OneLineIconListItem:
                            id: selectTest
                            text: "Test Screen"
                            IconLeftWidget:
                                icon: "menu"
"""
