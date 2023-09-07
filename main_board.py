import tkinter as tk


class ShogiBoard:
    def __init__(self, root):
        self.rows = 4
        self.cols = 3
        self.square_size = 300

        # Create canvas to draw the board
        self.canvas = tk.Canvas(root, width=self.cols*self.square_size,
                                height=self.rows*self.square_size, bg="white")
        self.canvas.pack()

        # Draw the squares on the board
        self.draw_board()

    def draw_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = "red" if (i+j) % 2 == 0 else "green"
                x1 = j * self.square_size
                y1 = i * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)


# Create the main window and instantiate the ShogiBoard class
root = tk.Tk()
root.title("Animal Shogi")
shogi_board = ShogiBoard(root)
root.mainloop()
