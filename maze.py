from cell import *
import time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = int((-1 * num_rows) if(num_rows < 0) else num_rows)
        self.num_cols = int((-1 * num_cols) if(num_cols < 0) else num_cols)
        self._win = win
        self._cells = []
        self.cell_size_x = self.get_cell_dim(True)
        self.cell_size_y = self.get_cell_dim()

        self._create_cells()

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
                current_row.append(Cell((i * self.cell_size_x), (j * self.cell_size_y), (i * self.cell_size_x) + self.cell_size_x, (j * self.cell_size_y) + self.cell_size_y, self._win))

            self._cells.append(current_row)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j]._draw()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

