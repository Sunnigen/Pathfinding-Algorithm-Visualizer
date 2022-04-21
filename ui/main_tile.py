from typing import Tuple

from kivy.lang.builder import Builder
from kivy.uix.behaviors import DragBehavior
from kivy.uix.label import Label

TILE_SIZE = 25


Builder.load_string("""
<Tile>:
    # Define the properties for the DragLabel
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    
    canvas:
        Color:
            rgba: 0.25, .1, .1, 0.25
        Rectangle:
            pos: self.pos
            size: self.size

""")


class Tile(DragBehavior, Label):
    size_hint = (None, None)
    being_dragged: bool = False
    tile_name: str = ""
    temp_coordinates: Tuple[int, int] = (-999, -999)

    def __init__(self,tile_name: str, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.text_size = self.size
        self.halign = 'center'
        self.valign = 'center'
        self.markup = True
        self.tile_name = tile_name

    def on_touch_down(self, touch):
        # Relative Position to Parent Widget
        # self.to_parent(x, y, relative=True) doesn't work as I think it does
        # x, y = touch.pos
        # x -= self.parent.x
        # y -= self.parent.y
        # x = max(min(int(x // TILE_SIZE), self.parent.grid_width - 1), 0)
        # y = max(min(int(y // TILE_SIZE), self.parent.grid_height - 1), 0)
        if self.collide_point(*touch.pos):
            self.being_dragged = True
            return True
        return super(Tile, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.being_dragged:
            # Normalize Movement to Snap to Grid
            # Note: Take offset value from parent location and add to tile location
            x, y = touch.pos
            x = int(TILE_SIZE * round(x//TILE_SIZE) + (self.parent.x % TILE_SIZE))
            y = int(TILE_SIZE * round(y//TILE_SIZE) + (self.parent.y % TILE_SIZE))

            # Keep Touch Move Within Parent Grid
            x = max(min(x, (self.parent.grid_width - 1) * TILE_SIZE + self.parent.x), self.parent.x)
            y = max(min(y, (self.parent.grid_height - 1) * TILE_SIZE + self.parent.y), self.parent.y)

            # Ensure that New Position isn't same as Start/Goal
            norm_x = int(round(x // TILE_SIZE) - (self.parent.x // TILE_SIZE))
            norm_y = int(round(y // TILE_SIZE) - (self.parent.y // TILE_SIZE))
            if ((norm_x, norm_y) == self.parent.start and self.tile_name != "start") or \
                    ((norm_x, norm_y) == self.parent.goal and self.tile_name != "goal"):
                return True

            self.temp_coordinates = (norm_x, norm_y)

            self.pos = (x, y)
            return True
        return super(Tile, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        self.being_dragged = False
        # print(f"{self.text} is no longer being dragged")

        # Update Main Coordinates
        if self.temp_coordinates != (-999, -999):
            if self.tile_name == "start":
                self.parent.start = self.temp_coordinates
            elif self.tile_name == "goal":
                self.parent.goal = self.temp_coordinates
            # Ensure Space is Open
            x, y = self.temp_coordinates
            self.parent.tiles_grid_state[x][y] = True
            self.parent.deactivate_tile(x, y)

        self.temp_coordinates = (-999, -999)
        return super(Tile, self).on_touch_up(touch)
