from cell import *
import time
import random
from cell_location import CellLocation
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, win, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = int((-1 * num_rows) if(num_rows < 0) else num_rows)
        self.num_cols = int((-1 * num_cols) if(num_cols < 0) else num_cols)
        self._win = win
        self._cells = []
        self.cell_size_x = self.get_cell_dim(True)
        self.cell_size_y = self.get_cell_dim()
        self.seed = seed

        if(seed):
            self.seed = random.seed(seed)

        # Adjust so that the maze is slightly smaller than the canvas and the surrounding window.
        self.cell_size_x = self.cell_size_x if(self.cell_size_x - 5 <= 10) else self.cell_size_x - 5.0
        self.cell_size_y = self.cell_size_y if(self.cell_size_y - 5 <= 10) else self.cell_size_y - 5.0

        self._create_cells()
        self._break_entrance_and_exit()

    def get_cell_dim(self, calc_width=False):
        if(self._win == None):
            return 1
        if(calc_width and self._win):
            if(self.num_cols == 0):
                raise Exception("Columns must be greater than 1.")
            return self._win.width / self.num_cols
        else:
            if(self.num_rows == 0):
                raise Exception("Rows must be greater than 1.")
            return self._win.height / self.num_rows
    

    def _create_cells(self):
        for i in range(self.num_cols):
            current_row = []
            for j in range(self.num_rows):
                current_row.append(Cell((i * self.cell_size_x) + 5, (j * self.cell_size_y) + 5, (i * self.cell_size_x) + self.cell_size_x + 5, (j * self.cell_size_y) + self.cell_size_y + 5, self._win))

            self._cells.append(current_row)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j]._draw()

    def _break_entrance_and_exit(self):
        if(self.num_cols > 0 and self.num_rows > 0):
            self._cells[0][0].has_top_wall = False
            self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False

            self._cells[0][0]._draw()
            self._cells[self.num_cols - 1][self.num_rows - 1]._draw()

    def break_connecting_walls(self, current_cell, dest_tuple):
        dest_cell = self._cells[dest_tuple[0]][dest_tuple[1]]

        match dest_tuple[2]:
            case CellLocation.LEFT:
                dest_cell.has_right_wall = False
                current_cell.has_left_wall = False
                dest_cell._draw()
                current_cell._draw()
                return
            case CellLocation.RIGHT:
                dest_cell.has_left_wall = False
                current_cell.has_right_wall = False
                dest_cell._draw()
                current_cell._draw()
                return
            case CellLocation.TOP:
                dest_cell.has_bottom_wall = False
                current_cell.has_top_wall = False
                dest_cell._draw()
                current_cell._draw()
                return
            case CellLocation.BOTTOM:
                dest_cell.has_top_wall = False
                current_cell.has_bottom_wall = False
                dest_cell._draw()
                current_cell._draw()
                return
            case _:
                return



    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit = []

            if(i - 1 >= 0):
                to_visit.append(tuple(i - 1, j, CellLocation.LEFT))
            if(i + 1 < self.num_cols):
                to_visit.append(tuple(i + 1, j, CellLocation.RIGHT))
            if(j - 1 >= 0):
                to_visit.append(tuple(i, j - 1, CellLocation.BOTTOM))
            if(j + 1 < self.num_rows):
                to_visit.append(tuple(i, j + 1, CellLocation.TOP))

            if(len(to_visit) == 0):
                self._cells[i][j]._draw()
                return
            else:
                next_cell = random.randrange(0, len(to_visit))
                self.break_connecting_walls(self._cells[i][j], to_visit[next_cell])              
                self._break_walls_r(to_visit[next_cell][0], to_visit[next_cell][1])
                self._reset_cells_visited()
    
    def _reset_cells_visited(self):
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self._cells[i][j].visited = False

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
    
    def path_is_clear(self, current_cell, dest_cell, location):
        match location:
            case CellLocation.LEFT:
                return (current_cell.has_left_wall == False and dest_cell.has_right_wall == False)
            case CellLocation.RIGHT:
                return (current_cell.has_right_wall == False and dest_cell.has_left_wall == False)
            case CellLocation.TOP:
                return (current_cell.has_top_wall == False and dest_cell.has_bottom_wall == False)
            case CellLocation.BOTTOM:
                return (current_cell.has_bottom_wall == False and dest_cell.has_top_wall == False)
            case _:
                return False
            
    def can_traverse_to_cell(self, current_cell, dest_i, dest_j, location):
        if(dest_i in range(0, self.num_cols) and dest_j in range(0, self.num_rows)):
            dest_cell = self._cells[dest_i][dest_j]
            return self.path_is_clear(current_cell, dest_cell, location) and dest_cell.visited == False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        current_cell = self._cells[i][j]
        self._animate()
        current_cell.visited = True

        if(current_cell == self._cells[self.num_cols - 1][self.num_rows - 1]):
            return True

        # Left Cell
        if(self.can_traverse_to_cell(current_cell, i - 1, j, CellLocation.LEFT)):
            current_cell.draw_move(self._cells[i - 1][j])

            if(self._solve_r(i - 1, j)):
                return True
            else:
                current_cell.draw_move(self._cells[i - 1][j], True)
            
        # Right Cell
        if(self.can_traverse_to_cell(current_cell, i + 1, j, CellLocation.RIGHT)):
            current_cell.draw_move(self._cells[i + 1][j])

            if(self._solve_r(i + 1, j)):
                return True
            else:
                current_cell.draw_move(self._cells[i + 1][j], True)
            
        # Top Cell
        if(self.can_traverse_to_cell(current_cell, i, j + 1, CellLocation.TOP)):
            current_cell.draw_move(self._cells[i][j + 1])

            if(self._solve_r(i, j + 1)):
                return True
            else:
                current_cell.draw_move(self._cells[i][j + 1], True)
            
        # Bottom Cell
        if(self.can_traverse_to_cell(current_cell, i - 1, j, CellLocation.BOTTOM)):
            current_cell.draw_move(self._cells[i][j - 1])

            if(self._solve_r(i, j - 1)):
                return True
            else:
                current_cell.draw_move(self._cells[i][j - 1], True)
                        
        return False




