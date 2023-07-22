from boardgame import BoardGame
from PIL import Image, ImageTk
import tkinter as tk


class Pokemon(BoardGame):
    def __init__(self):
        
        super().__init__(
            title = "Pokemon", 
            board_size=(9, 9), 
            board_boundary_ratio = 259/(449-259), 
            cell_size=None
        )

        # self.__set_background__()

    
    def __set_background__(self):
        img_path = "alternative_boardgames/pokemon/assets/pokemon-board-original-compressed.ae2a561b28e40cef94b8.png"
        background = Image.open(img_path)
        background = background.resize((self.board_geometry[1], self.board_geometry[0]))
        self.background = ImageTk.PhotoImage(background)
        self.board.create_image(0, 0, image=self.background, anchor=tk.NW)


if __name__ == "__main__":
    game = Pokemon()
    # game = BoardGame(board_size = (9,9), cell_size = None, board_boundary_ratio = 259/(449-259))
    game.mainloop()