import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, None)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_negative_dims(self):
        num_cols = -12
        num_rows = -10
        m1 = Maze(0, 0, num_rows, num_cols, None)
        self.assertEqual(
            len(m1._cells),
            -1 * num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            -1 * num_rows,
        )
    
    def test_maze_invalid_dims(self):
        num_cols = 0
        num_rows = -10

        num_cols2 = -10
        num_rows2 = 0

        # Invalid Columns
        self.assertRaises(Exception, Maze(0, 0, num_rows, num_cols, None))
        
        #Invalid Rows
        self.assertRaises(Exception, Maze(0, 0, num_rows2, num_cols2, None))

    def test_maze_decimal_dims(self):
        # Logic should round to nearest whole number.
        num_cols = 1.1
        num_rows = 1.8

        num_cols2 = 0.1
        num_rows2 = 0.1

        m1 = Maze(0, 0, num_rows, num_cols, None)
        self.assertEqual(
            len(m1._cells),
            1,
        )
        self.assertEqual(
            len(m1._cells[0]),
            1,
        )

        # Invalid Columns (Rounds down to 0)
        self.assertRaises(Exception, Maze(0, 0, num_rows, num_cols2, None))
        
        #Invalid Rows (Rounds down to 0)
        self.assertRaises(Exception, Maze(0, 0, num_rows2, num_cols, None))
    
    def test_break_entrance_and_exit(self):
        m1 = Maze(0, 0, 3, 3, None)
        
        self.assertEqual(False, m1._cells[0][0].has_top_wall)
        self.assertEqual(False, m1._cells[m1.num_cols - 1][m1.num_rows - 1].has_bottom_wall)

    def test_reset_visited(self):
        m1 = Maze(0, 0, 3, 3, None)
        
        for i in range(0, m1.num_cols):
            for j in range(0, m1.num_rows):
                m1._cells[i][j].visited = True

        for i in range(0, m1.num_cols):
            for j in range(0, m1.num_rows):
                self.assertEqual(m1._cells[i][j].visited, True)

        m1._reset_cells_visited()

        for i in range(0, m1.num_cols):
            for j in range(0, m1.num_rows):
                self.assertNotEqual(m1._cells[i][j].visited, True)

if __name__ == "__main__":
    unittest.main()
