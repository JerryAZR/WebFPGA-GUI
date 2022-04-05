synthkv = """
<SynthLayout>
    cols: 1
    padding: [0, 0, 0, 0]   # [left, top, right, bottom]
    active_color: app.theme_cls.primary_color
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
                        md_bg_color: root.active_color
                    MDFillRoundFlatIconButton:
                        id: rmAllFilesBtn
                        icon: "book-remove-multiple"
                        text: "Remove all"
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
    MDIconButton:
        id: deleteEntryBtn
        icon: "book-remove"
        root: root      # Make root available in python code

"""