from line import *
from point import *

class Cell:
    has_left_wall = True
    has_right_wall = True
    has_top_wall = True
    has_bottom_wall = True
    visited = False
            
    def get_midpoint(self):
        center_x = round((self._x1 + self._x2) / 2, 2)
        center_y =  round((self._y1 + self._y2) / 2, 2)
        return Point(center_x, center_y)

    def __init__(self, x1, y1, x2, y2, win):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self.center = self.get_midpoint()

    def _draw(self):
        if(self._x1 < self._x2 and self._y1 > self._y2):
            self.draw(self._x1, self._y1, self._x2, self._y2)
        else:
            self.draw(self._x2, self._y2, self._x1, self._y1)

    def draw(self, tl_x, tl_y, br_x, br_y):
        if(self._win == None):
            return

        t_point = Point(tl_x, tl_y)
        b_point = Point(tl_x, br_y)
        
        # Left Wall
        if(self.has_left_wall):
            Line(t_point, b_point).draw(self._win.canvas)
        else:
            Line(t_point, b_point).draw(self._win.canvas, fill_color="#d9d9d9")

        t_point = Point(br_x, tl_y)
        b_point = Point(br_x, br_y)
        
        # Right Wall
        if(self.has_right_wall):
            Line(t_point, b_point).draw(self._win.canvas)
        else:
            Line(t_point, b_point).draw(self._win.canvas, fill_color="#d9d9d9")

        t_point = Point(tl_x, tl_y)
        b_point = Point(br_x, tl_y)
        
        # Bottom Wall
        if(self.has_bottom_wall):
            Line(t_point, b_point).draw(self._win.canvas)
        else:
            Line(t_point, b_point).draw(self._win.canvas, fill_color="#d9d9d9")

        t_point = Point(tl_x, br_y)
        b_point = Point(br_x, br_y)
        
        # Top Wall
        if(self.has_top_wall):
            Line(t_point, b_point).draw(self._win.canvas)
        else:
            Line(t_point, b_point).draw(self._win.canvas, fill_color="#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        fill_colour = "gray" if(undo) else "red"

        if(not self == to_cell):
            Line(self.center, to_cell.center).draw(self._win.canvas, fill_colour)

    def __eq__(self, to_cell):
        return (self._x1 == to_cell._x1) and (self._y1 == to_cell._y1) and (self._x2 == to_cell._x2) and (self._y2 == to_cell._y2) 






