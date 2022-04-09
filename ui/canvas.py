from random import randint

from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from ui.main_tile import Tile

TILE_SIZE = 25

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
    pressed_tiles = set()
    dragging: bool = False
    start = (-999, -999)
    goal = (-999, -999)

    def __init__(self, grid_width, grid_height, **kwargs) -> None:
        super(Grid, self).__init__(**kwargs)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.line_grid = [[None for y in range(grid_height)] for x in range(grid_width)]
        self.tiles_grid_state = [[True for y in range(grid_height)] for x in range(grid_width)]
        self.tiles_grid = [[None for y in range(grid_height)] for x in range(grid_width)]
        self.rect = None
        self.place_start_goal()
        self.start_tile = Tile(size=(TILE_SIZE, TILE_SIZE), text='[b][color=#000000]S[/color][/b]')
        self.goal_tile = Tile(size=(TILE_SIZE, TILE_SIZE), text='[b][color=#000000]G[/color][/b]')
        self.start_tile.pos = (self.start[0] * TILE_SIZE, self.start[1] * TILE_SIZE)
        self.goal_tile.pos = (self.goal[0] * TILE_SIZE, self.goal[1] * TILE_SIZE)
        self.add_widget(self.start_tile)
        self.add_widget(self.goal_tile)

    def set_size(self) -> None:
        self.size = (self.grid_width * TILE_SIZE, self.grid_height * TILE_SIZE)

    def draw_grid(self) -> None:
        with self.canvas:
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    # Color(.1, .1, 1, 1.0)
                    Color(52/255, 73/255, 94/255, 1.0)
                    line = Line(width=1,
                                rectangle=(self.x + (x * TILE_SIZE),
                                           self.top - TILE_SIZE - (y * TILE_SIZE),
                                           TILE_SIZE,
                                           TILE_SIZE)
                                )
                    self.line_grid[x][y] = line
                    # Color(.1, .1, .1, 1.0)
                    rect = Rectangle(size=(0, 0), pos=(self.x + (x * TILE_SIZE), self.y + (y * TILE_SIZE)))
                    self.tiles_grid[x][y] = rect

    def update_grid(self) -> None:
        # print(self.x, self.y, self.right, self.top)
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                line = self.line_grid[x][y]
                line.rectangle = (self.x + (x * TILE_SIZE),
                                  self.top - TILE_SIZE - (y * TILE_SIZE),
                                  TILE_SIZE,
                                  TILE_SIZE)

                rect = self.tiles_grid[x][y]
                rect.pos = (self.x + (x * TILE_SIZE), self.y + (y * TILE_SIZE))
        self.start_tile.pos = (self.x + self.start[0] * TILE_SIZE, self.y + self.start[1] * TILE_SIZE)
        self.goal_tile.pos = (self.x + self.goal[0] * TILE_SIZE, self.y + self.goal[1] * TILE_SIZE)
        # self.rect.pos = self.pos
        # self.rect.size = self.size

    def print_tiles(self) -> None:
        for t_row in self.tiles:
            print(t_row)

    def on_size(self, *args) -> None:
        self.update_grid()

    def on_pos(self, *args) -> None:
        self.update_grid()

    def place_start_goal(self) -> None:
        # Select Unblocked Random Spots on Grid
        tries = 1000
        t = 0
        start = (-999, -999)
        goal = (-999, -999)
        while t < tries and (start == (-999, -999) or goal == (-999, -999)):

            start = (randint(0, self.grid_width - 1), randint(0, self.grid_height - 1))
            goal = (randint(0, self.grid_width - 1), randint(0, self.grid_height - 1))

            # Check if Start is Blocked
            try:
                if not self.tiles_grid_state[start[0]][start[1]]:
                    start = (-999, -999)


                # Check if Goal is Blocked
                if not self.tiles_grid_state[goal[0]][goal[1]]:
                    goal = (-999, -999)
            except IndexError as error:
                print(start, goal)

            t += 1
        self.start = start
        self.goal = goal

    def randomize_grid(self) -> None:
        self.clear_grid()
        for i in range(randint(self.grid_width * self.grid_height // 4, self.grid_width * self.grid_height // 2)):
            x = randint(0, self.grid_width - 1)
            y = randint(0, self.grid_height - 1)

            if (x, y) == self.start or (x, y) == self.goal:
                continue
            self.tiles_grid_state[x][y] = False
            self.activate_tile(x, y)

    def clear_grid(self) -> None:
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.deactivate_tile(x, y)
                self.tiles_grid_state[x][y] = True

        self.pressed_tiles.clear()

    def activate_tile(self, x, y) -> None:
        rect = self.tiles_grid[x][y]
        rect.size = TILE_SIZE, TILE_SIZE

    def deactivate_tile(self, x, y) -> None:
        rect = self.tiles_grid[x][y]
        rect.size = 0, 0

    def invert_tile(self, x, y) -> None:
        self.tiles_grid_state[x][y] = not self.tiles_grid_state[x][y]

    def on_touch_down(self, touch) -> None:
        x, y = self.to_widget(*touch.pos, relative=True)
        x = max(min(int(x // TILE_SIZE), self.grid_width - 1), 0)
        y = max(min(int(y // TILE_SIZE), self.grid_height - 1), 0)

        if self.start_tile.collide_point(*touch.pos):
            self.dragging = True
            return super(Grid, self).on_touch_down(touch)

        elif self.goal_tile.collide_point(*touch.pos):
            self.dragging = True
            return super(Grid, self).on_touch_down(touch)

        elif self.collide_point(*touch.pos) and (x, y) not in self.pressed_tiles:

            if (x, y) == self.start or (x, y) == self.goal:
                pass
            else:
                self.press_down = True
                self.invert_tile(x, y)
                self.pressed_tiles.add((x, y))

                if not self.tiles_grid_state[x][y]:
                    self.activate_tile(x, y)
                else:
                    self.deactivate_tile(x, y)
                # print("Touch down at ({}, {})".format(x, y))

    def on_touch_move(self, touch) -> None:
        x, y = self.to_widget(*touch.pos, relative=True)
        x = max(min(int(x // TILE_SIZE), self.grid_width - 1), 0)
        y = max(min(int(y // TILE_SIZE), self.grid_height - 1), 0)

        if self.dragging:
            return super(Grid, self).on_touch_move(touch)
        elif self.collide_point(*touch.pos) and (x, y) not in self.pressed_tiles:

            if (x, y) == self.start or (x, y) == self.goal:
                pass
            else:

                self.invert_tile(x, y)
                self.activate_tile(x, y)
                self.pressed_tiles.add((x, y))

                if not self.tiles_grid_state[x][y]:
                    self.activate_tile(x, y)
                else:
                    self.deactivate_tile(x, y)
                # print("Touch down at ({}, {})".format(x, y))

    def on_touch_up(self, touch) -> None:
        self.press_down = False
        self.dragging = False
        # self.start_tile.being_dragged = False
        # self.goal_tile.being_dragged = False
        if self.collide_point(*touch.pos):
            # print("Touch up at ({}, {})".format(*self.to_widget(*touch.pos, relative=True)))
            self.pressed_tiles.clear()
            # self.print_tiles()
        return super(Grid, self).on_touch_up(touch)


class GridAnchor(AnchorLayout):
    grid: Grid = None
    rect: Rectangle = None
    grid_width: int = 20
    grid_height: int = 20

    def __init__(self, grid_width, grid_height, **kwargs) -> None:
        super(GridAnchor, self).__init__(**kwargs)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.anchor_x = "center"
        self.anchor_y = "top"
        self.grid = Grid(grid_width, grid_height, size_hint=(None, None), pos_hint={"center_x": 0.5})
        self.add_widget(self.grid)

    def draw_grid(self) -> None:
        self.grid.draw_grid()
        self.grid.set_size()

    def clear_grid(self) -> None:
        self.grid.clear_grid()

    def randomize_grid(self) -> None:
        self.grid.randomize_grid()

    def on_size(self, *args) -> None:
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

        grid_width, grid_height = 25, 15

        self.g = GridAnchor(grid_width, grid_height, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(self.g)
        self.g.draw_grid()

    def on_size(self, *args) -> None:
        if self.g:
            self.g.on_size()

    def clear_grid(self) -> None:
        self.g.clear_grid()

    def randomize_grid(self) -> None:
        self.g.randomize_grid()
