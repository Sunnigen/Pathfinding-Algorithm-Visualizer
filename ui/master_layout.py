from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


from ui.canvas import Body
from ui.top_nav_bar import TopNavBar


class AStarApp(App):
    def build(self):
        b = BoxLayout(size_hint=(1, 1), orientation='vertical')
        nav_bar = TopNavBar(size_hint=(1, 0.2))
        grid = Body(nav_bar=nav_bar, size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0})
        nav_bar.grid = grid
        b.add_widget(nav_bar)
        b.add_widget(grid)
        return b
