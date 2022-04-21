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
            
    BoxLayout:
        orientation: "horizontal"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        
        Button:
            text: "Clear Grid"
            size_hint: (0.2, 1)
            on_press: root.clear_grid()
            
        Button:
            text: 'Randomize Grid'
            size_hint: (0.2, 1)
            on_press: root.randomize_grid()
            
        Button:
            text: "Find Path!"
            size_hint:  (0.2, 1)
            on_press: root.pathfind()
""")


class TopNavBar(FloatLayout):
    grid = None

    def __init__(self,  **kwargs):
        super(TopNavBar, self).__init__(**kwargs)
        label = Label(text="TopNavBar", pos_hint={'x': 0, 'top': 1}, size_hint=(None, None))
        label.text_size = label.size
        label.halign = 'left'
        label.valign = 'top'
        self.add_widget(label)

    def clear_grid(self) -> None:
        self.grid.clear_grid()

    def randomize_grid(self) -> None:
        self.grid.randomize_grid()

    def set_grid(self, grid):
        self.grid = grid

    def pathfind(self) -> None:
        self.grid.pathfind()
