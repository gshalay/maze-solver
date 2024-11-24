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

if __name__ == "__main__":
    unittest.main()
