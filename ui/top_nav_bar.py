from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


Builder.load_string("""
<TopNavBar>:
    canvas:
        Color:
            rgba: 52/255, 73/255, 94/255, 1.0
        Rectangle:
            pos: self.pos
            size: self.size
""")


class TopNavBar(FloatLayout):
    def __init__(self, **kwargs):
        super(TopNavBar, self).__init__(**kwargs)
        label = Label(text="TopNavBar", pos_hint={'x': 0, 'top': 1}, size_hint=(None, None))
        label.text_size = label.size
        label.halign = 'left'
        label.valign = 'top'
        self.add_widget(label)

        # with self.canvas:
        #     Color(1, 0, 0, 0.5)
        #     Rectangle(size=self.size)
