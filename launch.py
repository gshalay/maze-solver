from window import *
from line import *
from point import *
from cell import *
from maze import *

def launch():
    main_window = Window(600, 600)

    board = Maze(0, 0, 6, 6, main_window)
    board._animate()
    
    # # Vertical move.
    # vert1 = Cell(50, 200, 150, 100, main_window)
    # vert1.has_bottom_wall = False
    # vert1.draw(vert1._x1, vert1._y1, vert1._x2, vert1._y2)

    # vert2 = Cell(50, 350, 150, 250, main_window)
    # vert2.has_top_wall = False
    # vert2.draw(vert2._x1, vert2._y1, vert2._x2, vert2._y2)

    # vert1.draw_move(vert2)


    # # Vertical move.
    # vert3 = Cell(200, 150, 300, 300, main_window)
    # vert3.has_right_wall = False
    # vert3.draw(vert3._x1, vert3._y1, vert3._x2, vert3._y2)

    # vert4 = Cell(400, 150, 500, 300, main_window)
    # vert4.has_left_wall = False
    # vert4.draw(vert4._x1, vert4._y1, vert4._x2, vert4._y2)

    # vert3.draw_move(vert4)

    main_window.wait_for_close()

if(__name__ == "__main__"):
    launch()