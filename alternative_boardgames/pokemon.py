from boardgame import BoardGame
from PIL import Image, ImageTk
import tkinter as tk


class Pokemon(BoardGame):
    def __init__(self):
        self.player_types = []

        super().__init__(
            title = "Pokemon", 
            board_size=(9, 9), 
            board_boundary_ratio = 259/(449-259), 
            cell_size=None
        )

        

    
    def __set_background__(self):
        img_path = "alternative_boardgames/pokemon/assets/pokemon-board-original-compressed.ae2a561b28e40cef94b8.png"
        background = Image.open(img_path)
        background = background.resize((self.board_geometry[1], self.board_geometry[0]))
        self.background = ImageTk.PhotoImage(background)
        self.board.create_image(0, 0, image=self.background, anchor=tk.NW)

    def draw_board(self):
        # Draw the board grid and player
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                if row in [3,4,5] or col in [3,4,5]:
                    continue
                x0, y0 = self.board_boundary_size[0] + col * self.cell_size, self.board_boundary_size[1] + row * self.cell_size
                x1, y1 = x0 + self.cell_size-1, y0 + self.cell_size-1
                self.board.create_rectangle(x0, y0, x1, y1, outline="black", width = 1)

    # def create_widgets(self):
    #     super().create_widgets()

    #     # add pokemon  next to player name
    #     img = Image.open("alternative_boardgames/pokemon/assets/pikachu.png")
    #     img = img.resize((self.token_size, self.token_size))
    #     img = ImageTk.PhotoImage(img)
    #     self.player_board.

    def create_player(self):
        d = super().create_player()
        d["type"] = "water"

        # calculate values for the player board
        player_id = len(self.players)
        r = self.token_size // 2
        c1, c2 = r + 5, 2*(r+5)*(player_id+1)

        # add pokemon  next to player name
        img = Image.open("alternative_boardgames/pokemon/assets/water-type.png")
        img = img.resize((self.token_size, self.token_size))
        self.player_types.append(ImageTk.PhotoImage(img))
        self.player_board.create_image(200-self.token_size, c2-r, image=self.player_types[player_id], anchor=tk.NW)


        return d

    # def create_dice(self):
    #     self.roll_button = tk.Button(self, text="Roll Dice", command=self.roll_dice)
    #     self.roll_button.pack(side = tk.LEFT, padx=10, pady=10)

if __name__ == "__main__":
    game = Pokemon()
    # game = BoardGame(board_size = (9,9), cell_size = None, board_boundary_ratio = 259/(449-259))
    game.mainloop()