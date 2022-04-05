flashkv = """
<FlashLayout>:
    cols: 1
    adaptive_height: True
    spacing: 16
    padding: 16
    active_color: app.theme_cls.primary_color
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
    MDTextField:
        id: bitstream
        text: "bitstream.bin"
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
                md_bg_color: root.active_color
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            MDFillRoundFlatIconButton:
                id: flashBtn
                icon: "usb-port"
                text: "Program FPGA"
                disabled: False
                md_bg_color: (100, 100, 100) if flashBtn.disabled else root.active_color

"""