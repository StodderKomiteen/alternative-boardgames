import tkinter as tk
from tkinter.colorchooser import askcolor

from random import randint
from utils import get_screen_size, resizeImage
from PIL import Image, ImageTk


class BoardGame(tk.Tk):
    def __init__(self, 
        title = "Board Game with Dice",  # Title of the game
        board_size=(10, 10),  # Size of the board as WxH, e.g. (10, 10) for 10x10 board with 100 fields
        board_boundary_ratio = 1,  # Size of the boundary around the board, given as a fraction of the cell size
        cell_size=None,  # Size of each cell in the board, must be int as cells are squares
        num_players = 2,  # Number of players in the game
        # background = None  # Background image of the board
    ):
        super().__init__()

        self.__setconstants__()
        self.__bind_keys__()

        # Create screen
        self.title(title)
        # self.toggle_fullscreen()
        self.geometry(f"{self.__screen_size__[0]}x{self.__screen_size__[1]}")

        # Initialize board game values
        self.board_size = board_size if not isinstance(board_size, int) else (board_size, board_size)
        self.board_boundary_ratio = board_boundary_ratio
        self.cell_size = cell_size if cell_size is not None else int(min(self.__screen_size__[0]/(self.board_size[0] + 2*self.board_boundary_ratio), self.__screen_size__[1]/(self.board_size[1] + 2*self.board_boundary_ratio)))
        self.token_size = int(self.cell_size *0.25) # Diameter of the token
        self.board_boundary_size = (int(self.board_boundary_ratio*self.cell_size), int(self.board_boundary_ratio*self.cell_size))
        self.board_geometry = (self.cell_size*self.board_size[1]+2*self.board_boundary_size[0], self.cell_size*self.board_size[0]+2*self.board_boundary_size[1])
        # self.player_position = 0

        self.num_players = num_players
        self.players = []
        

        # Create the game board
        # self.player_position = 1
        self.create_widgets()

    def __setconstants__(self):
        self.__screen_size__ = get_screen_size()
        # self.__screen_size__ = (self.__screen_size__[0], self.__screen_size__[1] - 50)

    def __set_background__(self):
        pass

    def create_widgets(self):
        # Create the game board
        self.board = tk.Canvas(self, width=self.board_geometry[0], height=self.board_geometry[1], bg="white")
        self.__set_background__()
        self.board.pack()

        # Draw the game board
        self.draw_board()

        # Create the players
        # self.player_board = tk.Text(self, width=20, height=(self.num_players+1)*self.token_size)
        # self.player_board.place(x=self.token_size*2, y=self.token_size*2)
        self.player_board_title = tk.Canvas(self, width=200, height=30, bg="white")
        self.player_board_title.place(x=self.token_size*2, y=self.token_size*2)
        self.player_board_title.create_text(0, 0, text="Players", font=("Arial", 14), fill="black", anchor=tk.NW)
        self.player_board = tk.Canvas(self, width=200, height=(self.num_players+1)*(self.token_size+10), bg="white")
        self.player_board.place(x=self.token_size*2, y=30 + self.token_size*2)

        for _ in range(self.num_players):
            self.players.append(self.create_player())
        for player_id in range(len(self.players)):
            self.draw_player(player_id)


        # Create the dice roll button
        self.create_dice()

        

    def create_dice(self):
        # Create the dice roll button
        self.roll_button = tk.Button(self, text="Roll Dice", command=self.roll_dice)
        self.roll_button.place(x=(self.__screen_size__[0]-self.board_geometry[0]) // 2 - 50 -10, y=self.__screen_size__[1]//2, width=50, height=50)


    def draw_board(self):
        # Draw the board grid and player
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                x0, y0 = self.board_boundary_size[0] + col * self.cell_size, self.board_boundary_size[1] + row * self.cell_size
                x1, y1 = x0 + self.cell_size-1, y0 + self.cell_size-1
                self.board.create_rectangle(x0, y0, x1, y1, outline="black", width = 1)


    # def create_player(self, name, image_path = None):
    def create_player(self):
        # color = askcolor(title ="Choose color")
        # color = color[1] # convert to hex
        player_id = len(self.players)

        color = "blue" if player_id == 0 else "red"

        name = "Player" + str(player_id + 1)

        # display the player name and token
        # self.board.create_text(self.__screen_size__[0] - 100, 50, text=name, font=("Arial", 16), fill=color)
        # self.board.create_text(self.__screen_size__[0] - 100, 50 + len(self.players) * 50, text=name, font=("Arial", 16), fill=color)
        # self.player_board.insert(tk.END, name + "\n")
        r = self.token_size // 2
        # self.board.create_oval(r, r, 2*r, 2*r, fill=color)
        c1, c2 = r + 5, 2*(r+5)*(player_id+1)
        self.player_board.create_oval(c1-r, c2-r, c1+r, c2+r, fill=color)
        self.player_board.create_text(c1+2*r, c2-r+2.5, text=name, font=("Arial", r), fill="black", anchor=tk.NW)
        # self.player_board.create_text(2*r, 3*r*(player_id+1), text=name, font=("Arial", r), fill="black", anchor=tk.NW)

        return {
            "name": name,
            "position": 0,
            "color" : color,
        }
    
    def draw_player(self, player_id):
        player = self.players[player_id]
        x0, y0 = self.position_to_coordinates(player["position"])
        r = self.token_size // 2
        self.players[player_id]["token"] = self.board.create_oval(x0-r, y0-r, x0+r, y0+r, fill=player["color"])

    def move_player(self, steps, player_id):
        # Move the player on the board
        self.board.delete(self.players[player_id]["token"])

        self.players[player_id]["position"] += steps
        if self.players[player_id]["position"] > self.board_size[0] * self.board_size[1]:
            self.players[player_id]["position"] = self.board_size[0] * self.board_size[1]
        
        self.draw_player(player_id)

    def position_to_coordinates(self, position):
        row = (position ) // self.board_size[0]
        col = (position ) % self.board_size[0]
        x0 = self.board_boundary_size[0] + col * self.cell_size + self.cell_size // 2
        y0 = self.board_boundary_size[0] + row * self.cell_size + self.cell_size // 2

        # add some randomness to the position
        x0 += randint(-self.cell_size//4, self.cell_size//4)
        y0 += randint(-self.cell_size//4, self.cell_size//4)
        return (x0, y0)

    # def draw_player(self, position):
    #     player_row = (self.player_position ) // self.board_size[0]
    #     player_col = (self.player_position ) % self.board_size[0]
    #     x0 = self.board_boundary_size[0] + player_col * self.cell_size + self.cell_size // 2
    #     y0 = self.board_boundary_size[0] + player_row * self.cell_size + self.cell_size // 2
    #     self.player_token = self.board.create_oval(x0-10, y0-10, x0+10, y0+10, fill="blue")

    # def move_player(self, steps):
    #     # Move the player on the board
    #     self.board.delete(self.player_token)

    #     self.player_position += steps
    #     if self.player_position > self.board_size[0] * self.board_size[1]:
    #         self.player_position = self.board_size[0] * self.board_size[1]
        
    #     self.draw_player(self.player_position)

    def roll_dice(self):
        # Simulate rolling the dice and move the player
        dice_roll = randint(1, 6)
        self.move_player(dice_roll, 0)

    def __bind_keys__(self):
        # Bind the F11 key to toggle full-screen mode
        self.bind("<F11>", self.toggle_fullscreen)
        
        # Bind the Escape key to exit full-screen mode
        self.bind("<Escape>", self.exit_fullscreen)

    def toggle_fullscreen(self, event=None):
        state = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not state)
        
    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

if __name__ == "__main__":
    # game = BoardGame(board_size = (9,9), cell_size = None, board_boundary_ratio = 259/(449-259), background = "alternative_boardgames/pokemon/assets/pokemon-board-original-compressed.ae2a561b28e40cef94b8.png")
    game = BoardGame(board_size = (9,11), cell_size = None, board_boundary_ratio = 259/(449-259), num_players=10)
    game.mainloop()
   
