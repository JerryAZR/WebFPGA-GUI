synthkv = """
<SynthLayout>
    cols: 1
    padding: [0, 0, 0, 0]   # [left, top, right, bottom]
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
                    MDFillRoundFlatIconButton:
                        id: rmAllFilesBtn
                        icon: "book-remove-multiple"
                        text: "Remove all"
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
                        active: True

    ScrollView:
        MDGridLayout:
            cols: 1
            id: fileListLayout
            adaptive_height: True

<FileEntry>:
    rows: 1
    adaptive_height: True
    padding: [8, 0]     # [horizontal, vertical]
    MDLabel:
        id: fileNameLabel
    MDIconButton:
        id: deleteEntryBtn
        icon: "book-remove"
        root: root      # Make root available in python code

"""