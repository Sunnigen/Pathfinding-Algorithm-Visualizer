from kivy.graphics import Color, Line, Rectangle
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label

TILE_SIZE = 50

Builder.load_string("""
<Body>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1.0
        Rectangle:
            pos: self.pos
            size: self.size
""")


class Grid(Widget):
    press_down: bool = False

    def __init__(self, grid_width, grid_height, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.line_grid = [[None for y in range(grid_height)] for x in range(grid_width)]
        self.rect = None

    def set_size(self):
        self.size = (self.grid_width * TILE_SIZE, self.grid_height * TILE_SIZE)

    def draw_grid(self):
        with self.canvas:
            Color(.1, .1, 1, .9)
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    line = Line(width=1,
                                rectangle=(self.x + (x * TILE_SIZE),
                                           self.top - TILE_SIZE - (y * TILE_SIZE),
                                           TILE_SIZE,
                                           TILE_SIZE)
                                )
                    self.line_grid[x][y] = line

            Color(1, 0, 0, 0.1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_grid(self):
        print(self.x, self.y, self.right, self.top)
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                line = self.line_grid[x][y]
                line.rectangle = (self.x + (x * TILE_SIZE),
                                  self.top - TILE_SIZE - (y * TILE_SIZE),
                                  TILE_SIZE,
                                  TILE_SIZE)
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_size(self, *args):
        self.update_grid()

    def on_pos(self, *args):
        self.update_grid()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.press_down = True
            print("Touch down at ({}, {})".format(*touch.pos))

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and self.press_down:
            # print("Touch move at ({}, {})".format(*touch.pos))
            pass

    def on_touch_up(self, touch):
        self.press_down = False
        if self.collide_point(*touch.pos):
            print("Touch up at ({}, {})".format(*touch.pos))


class GridAnchor(AnchorLayout):
    grid: Grid = None
    rect: Rectangle = None
    grid_width: int = 20
    grid_height: int = 20

    def __init__(self, grid_width, grid_height, **kwargs):
        super(GridAnchor, self).__init__(**kwargs)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.anchor_x = "center"
        self.anchor_y = "top"
        self.grid = Grid(grid_width, grid_height, size_hint=(None, None), pos_hint={"center_x": 0.5})
        self.add_widget(self.grid)

    def draw_grid(self):
        self.grid.draw_grid()
        self.grid.set_size()

    def on_size(self, *args):
        self.grid.on_size()


class Body(FloatLayout):
    g: GridAnchor = None

    def __init__(self, nav_bar, **kwargs):
        self.nav_bar = nav_bar
        super(Body, self).__init__(**kwargs)
        label = Label(text='[color=000000]Canvas[/color]', pos_hint={'x': 0, 'y': 0}, size_hint=(None, None),
                      markup=True)
        label.text_size = label.size
        label.halign = 'left'
        label.valign = 'bottom'
        self.add_widget(label)

        grid_width, grid_height = 10, 9

        self.g = GridAnchor(grid_width, grid_height, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(self.g)
        self.g.draw_grid()

    def on_size(self, *args):
        if self.g:
            self.g.on_size()
