from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.title = "Maze Solver"
        self.root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(width=width, height=height)
        self.is_running = False
        self.root.geometry(str(width) + "x" + str(height))

        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True

        while self.is_running:
            self.redraw()
    
    def close(self):
        self.is_running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)