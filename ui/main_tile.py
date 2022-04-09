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

    def __init__(self, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.text_size = self.size
        self.halign = 'center'
        self.valign = 'center'
        self.markup = True

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

            self.pos = (x, y)
            return True
        return super(Tile, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        self.being_dragged = False
        # print(f"{self.text} is no longer being dragged")
        return super(Tile, self).on_touch_up(touch)
