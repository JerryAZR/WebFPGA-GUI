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
            Widget:
            # Button:
            #     id: forwardBtn
            #     size_hint_y: None
            #     height: self.font_size * 3
            #     text: "Next step"
            #     on_release: root.forward()
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