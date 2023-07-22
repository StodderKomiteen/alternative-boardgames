import tkinter as tk
from random import randint
from utils import get_screen_size, resizeImage
from PIL import Image, ImageTk

class Cell:
    def __init__(self, size) -> None:
        self.size = size

class BoardGame(tk.Tk):
    def __init__(self, 
        title = "Board Game with Dice",  # Title of the game
        board_size=(10, 10),  # Size of the board as WxH, e.g. (10, 10) for 10x10 board with 100 fields
        board_boundary_ratio = 1,  # Size of the boundary around the board, given as a fraction of the cell size
        cell_size=None,  # Size of each cell in the board, must be int as cells are squares
        # background = None  # Background image of the board
    ):
        super().__init__()

        self.__setconstants__()

        # Create screen
        self.title(title)
        # self.attributes("-fullscreen", True)
        self.geometry(f"{self.__screen_size__[0]}x{self.__screen_size__[1]}")

        # Initialize board game values
        self.board_size = board_size if not isinstance(board_size, int) else (board_size, board_size)
        self.board_boundary_ratio = board_boundary_ratio
        self.cell_size = cell_size if cell_size is not None else int(min(self.__screen_size__[0]/(self.board_size[0] + 2*self.board_boundary_ratio), self.__screen_size__[1]/(self.board_size[1] + 2*self.board_boundary_ratio)))
        self.board_boundary_size = (int(self.board_boundary_ratio*self.cell_size), int(self.board_boundary_ratio*self.cell_size))
        self.board_geometry = (self.cell_size*self.board_size[0]+2*self.board_boundary_size[0], self.cell_size*self.board_size[1]+2*self.board_boundary_size[1])
        self.player_position = 1

        # Create the game board
        # self.player_position = 1
        self.create_widgets()

    def __setconstants__(self):
        self.__screen_size__ = get_screen_size()

    def __set_background__(self):
        pass

    def create_widgets(self):
        # Create the game board
        self.board = tk.Canvas(self, width=self.board_geometry[1], height=self.board_geometry[0], bg="white")
        self.__set_background__()
        self.board.pack()

        # Draw the game board
        self.draw_board()

        # Create the dice roll button
        self.roll_button = tk.Button(self, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack()


    def draw_board(self):
        # Draw the board grid and player
        
        
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                if row in [3,4,5] or col in [3,4,5]:
                    continue
                x0, y0 = self.board_boundary_size[0] + col * self.cell_size, self.board_boundary_size[1] + row * self.cell_size
                x1, y1 = x0 + self.cell_size-1, y0 + self.cell_size-1
                self.board.create_rectangle(x0, y0, x1, y1, outline="black", width = 1)

        self.draw_player(self.player_position)

    def draw_player(self, position):
        player_row = (self.player_position - 1) // self.board_size[0]
        player_col = (self.player_position - 1) % self.board_size[0]
        x0 = self.board_boundary_size[0] + player_col * self.cell_size + self.cell_size // 2
        y0 = self.board_boundary_size[0] + player_row * self.cell_size + self.cell_size // 2
        self.player_token = self.board.create_oval(x0-10, y0-10, x0+10, y0+10, fill="blue")

    def move_player(self, steps):
        # Move the player on the board
        self.board.delete(self.player_token)

        self.player_position += steps
        if self.player_position > self.board_size[0] * self.board_size[1]:
            self.player_position = self.board_size[0] * self.board_size[1]
        
        self.draw_player(self.player_position)

    def roll_dice(self):
        # Simulate rolling the dice and move the player
        dice_roll = randint(1, 6)
        self.move_player(dice_roll)

if __name__ == "__main__":
    # game = BoardGame(board_size = (9,9), cell_size = None, board_boundary_ratio = 259/(449-259), background = "alternative_boardgames/pokemon/assets/pokemon-board-original-compressed.ae2a561b28e40cef94b8.png")
    game = BoardGame(board_size = (9,11), cell_size = None, board_boundary_ratio = 259/(449-259))
    game.mainloop()
   
