from window import *
from line import *
from point import *
from cell import *
from maze import *

def launch():
    main_window = Window(600, 600)

    board = Maze(0, 0, 6, 6, main_window)
    board.solve()
    main_window.wait_for_close()

if(__name__ == "__main__"):
    launch()