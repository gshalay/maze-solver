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
            random.seed(seed)
            self.seed = random.random()

        # Adjust so that the maze is slightly smaller than the canvas and the surrounding window.
        self.cell_size_x = self.cell_size_x if(self.cell_size_x - 5 <= 10) else self.cell_size_x - 5.0
        self.cell_size_y = self.cell_size_y if(self.cell_size_y - 5 <= 10) else self.cell_size_y - 5.0

        self._create_cells()
        if(len(self._cells) > 2):
            self._break_walls_r(0, 0)
        #self._break_entrance_and_exit()
        self._reset_cells_visited()

    def get_cell_dim(self, calc_width=False):
        if(self._win == None):
            return 0
        if(calc_width and self._win):
            if(self.num_cols == 0):
                raise Exception("Columns must be greater than 1.")
            return self._win.width / self.num_cols
        else:
            if(self.num_rows == 0):
                raise Exception("Rows must be greater than 1.")
            return self._win.height / self.num_rows
    

    def find_cell_idx(self, search_cell):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                if(self._cells[i][j] == search_cell):
                    return (i, j)

    def _create_cells(self):
        for i in range(self.num_cols):
            current_row = []
            for j in range(self.num_rows):
                current_row.append(Cell((i * self.cell_size_x) + 5, (j * self.cell_size_y) + 5, (i * self.cell_size_x) + self.cell_size_x + 5, (j * self.cell_size_y) + self.cell_size_y + 5, self._win))

            if(current_row):
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

                coords = self.find_cell_idx(current_cell)
                print(f"\nBreaking left wall of Source Cell[{coords[0]}, {coords[1]}]")
                print(f"Breaking right wall of Dest Cell[{dest_tuple[0]}, {dest_tuple[1]}]\n")

                dest_cell._draw()
                current_cell._draw()
                return
            case CellLocation.RIGHT:
                dest_cell.has_left_wall = False
                current_cell.has_right_wall = False

                coords = self.find_cell_idx(current_cell)
                print(f"\nBreaking right wall of Source Cell[{coords[0]}, {coords[1]}]")
                print(f"Breaking left wall of Dest Cell[{dest_tuple[0]}, {dest_tuple[1]}]\n")
                
                dest_cell._draw()
                current_cell._draw()
                return
            case CellLocation.TOP:
                dest_cell.has_bottom_wall = False
                current_cell.has_top_wall = False

                coords = self.find_cell_idx(current_cell)
                print(f"\nBreaking top wall of Source Cell[{coords[0]}, {coords[1]}]")
                print(f"Breaking bottom wall of Dest Cell[{dest_tuple[0]}, {dest_tuple[1]}]\n")

                dest_cell._draw()
                current_cell._draw()
                return
            case CellLocation.BOTTOM:
                dest_cell.has_top_wall = False
                current_cell.has_bottom_wall = False

                coords = self.find_cell_idx(current_cell)
                print(f"\nBreaking bottom wall of Source Cell[{coords[0]}, {coords[1]}]")
                print(f"Breaking top wall of Dest Cell[{dest_tuple[0]}, {dest_tuple[1]}]\n")

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
                # move_info = (i - 1, j, CellLocation.LEFT)
                if(not self._cells[i - 1][j].visited and not self.cell_has_minimum_walls(self._cells[i - 1][j]) and not self.is_cell_left_maze_boundary(i - 1)):
                    print(f"Source Cell [{i}, {j}] has a valid left move to Dest Cell[{i - 1}, {j}]")
                    to_visit.append((i - 1, j, CellLocation.LEFT))
            if(i + 1 < self.num_cols):
                if(not self._cells[i + 1][j].visited and not self.cell_has_minimum_walls(self._cells[i + 1][j]) and not self.is_cell_right_maze_boundary(i + 1)):
                    print(f"Source Cell [{i}, {j}] has a valid right move to Dest Cell[{i + 1}, {j}]")
                    to_visit.append((i + 1, j, CellLocation.RIGHT))
            if(j - 1 >= 0):
                if(not self._cells[i][j - 1].visited and not self.cell_has_minimum_walls(self._cells[i][j - 1]) and not self.is_cell_top_maze_boundary(j - 1)):
                    print(f"Source Cell [{i}, {j}] has a valid top move to Dest Cell[{i}, {j - 1}]")
                    to_visit.append((i, j - 1, CellLocation.TOP))
            if(j + 1 < self.num_rows):
                if(not self._cells[i][j + 1].visited and not self.cell_has_minimum_walls(self._cells[i][j + 1]) and not self.is_cell_bottom_maze_boundary(j + 1)):
                    print(f"Source Cell [{i}, {j}] has a valid bottom move to Dest Cell[{i}, {j + 1}]")
                    to_visit.append((i, j + 1, CellLocation.BOTTOM))

            print(f"\nto_visit{to_visit}\n")

            if(not to_visit or (i == self.num_cols - 1 and j == self.num_rows - 1)):
                self._cells[i][j]._draw()
                return
            else:
                while to_visit:
                    next_cell = random.choice(to_visit)
                    to_visit.remove(next_cell)
                    if not self._cells[next_cell[0]][next_cell[1]].visited and not self.cell_has_minimum_walls(self._cells[next_cell[0]][next_cell[1]]):
                        self.break_connecting_walls(self._cells[i][j], next_cell)
                        self._break_walls_r(next_cell[0], next_cell[1])
    
    # By default, We want the minimum to be 1. 
    def cell_has_minimum_walls(self, current_cell):
        return sum([current_cell.has_left_wall, current_cell.has_right_wall, current_cell.has_top_wall, current_cell.has_bottom_wall]) <= 1

    def is_cell_left_maze_boundary(self, i):
        return i == 0
    
    def is_cell_right_maze_boundary(self, i):
        return i == self.num_cols - 1
    
    def is_cell_top_maze_boundary(self, j):
        return j == 0

    def is_cell_bottom_maze_boundary(self, j):
        return j == self.num_rows - 1

    def is_cell_maze_boundary(self, i, j):
        return (self.is_cell_left_maze_boundary(i) or self.is_cell_right_maze_boundary(i) or 
                self.is_cell_top_maze_boundary(j) or self.is_cell_bottom_maze_boundary(j)) 

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
        if(self.can_traverse_to_cell(current_cell, j - 1, j, CellLocation.TOP)):
            current_cell.draw_move(self._cells[i][j - 1])

            if(self._solve_r(i, j - 1)):
                return True
            else:
                current_cell.draw_move(self._cells[i][j - 1], True)

        # Bottom Cell
        if(self.can_traverse_to_cell(current_cell, i, j + 1, CellLocation.BOTTOM)):
            current_cell.draw_move(self._cells[i][j + 1])

            if(self._solve_r(i, j + 1)):
                return True
            else:
                current_cell.draw_move(self._cells[i][j + 1], True)
                        
        return False


