# Inspired by https://www.pokemondrinkinggame.com/


from boardgame import BoardGame
from PIL import Image, ImageTk
import tkinter as tk
from random import randint


class Pokemon(BoardGame):
    turn_marker_path = "alternative_boardgames/pokemon/assets/pokeball_25x25.png"

    def __init__(self, num_players = 2):
        # self.player_types = []

        

        # create order to move in
        self.__set_position_coords__()

        super().__init__(
            title = "Pokemon", 
            board_size=(9, 9), 
            board_boundary_ratio = 259/(449-259), 
            cell_size=None,
            num_players=num_players,
        )

        # add pokemon types
        self.player_types = ["water", "fire", "grass", "electric"]
        self.player_type_tokens = {}
        for t in self.player_types:
            img = Image.open(f"alternative_boardgames/pokemon/assets/{t}-type.png")
            img = img.resize((self.token_size, self.token_size))
            self.player_type_tokens[t] = ImageTk.PhotoImage(img)



    def __set_position_coords__(self):
        cell_order = []
        cell_order.extend([(i, 0) for i in range(8, -1, -1)]) # (8,0) -> (0,0)
        cell_order.extend([(0, i) for i in range(1, 9)]) # (0,1) -> (0,8)
        cell_order.extend([(i, 8) for i in range(1, 9)]) # (1,8) -> (8,8)
        cell_order.extend([(8, i) for i in range(7, 0, -1)]) # (8,7) -> (8,1)
        cell_order.extend([(i, 1) for i in range(7, 0, -1)]) # (7,1) -> (1,1)
        cell_order.extend([(1, i) for i in range(2, 8)]) # (1,2) -> (1,7)
        cell_order.extend([(i, 7) for i in range(2, 8)]) # (2,7) -> (7,7)
        cell_order.extend([(7, i) for i in range(6, 1, -1)]) # (7,6) -> (7,2)
        cell_order.extend([(i, 2) for i in range(6, 1, -1)]) # (6,2) -> (2,2)
        cell_order.extend([(2, i) for i in range(3, 7)]) # (2,3) -> (2,6)
        cell_order.extend([(i, 6) for i in range(3, 7)]) # (3,6) -> (6,6)
        cell_order.extend([(6, i) for i in range(5, 2, -1)]) # (6,5) -> (6,3)
        cell_order.extend([(4,4)])

        # cell_order.extend([(8, i) for i in range(9)])

        self.cell_order = cell_order

    def position_to_coordinates(self, position):
        # row = (position ) // self.board_size[0]
        # col = (position ) % self.board_size[0]
        row, col = self.cell_order[position]
        
        x0 = self.board_boundary_size[0] + col * self.cell_size + self.cell_size // 2
        y0 = self.board_boundary_size[0] + row * self.cell_size + self.cell_size // 2

        # add some randomness to the position
        x0 += randint(-self.cell_size//4, self.cell_size//4)
        y0 += randint(-self.cell_size//4, self.cell_size//4)
        return (x0, y0)

    
    def __set_background__(self):
        img_path = "alternative_boardgames/pokemon/assets/pokemon-board-original-compressed.ae2a561b28e40cef94b8.png"
        background = Image.open(img_path)
        background = background.resize((self.board_geometry[1], self.board_geometry[0]))
        self.background = ImageTk.PhotoImage(background)
        self.board.create_image(0, 0, image=self.background, anchor=tk.NW)

    def draw_board(self):
        pass 
        # # Draw the board grid and player
        # for row in range(self.board_size[0]):
        #     for col in range(self.board_size[1]):
        #         if row in [3,4,5] and col in [3,4,5]:
        #             continue
        #         x0, y0 = self.board_boundary_size[0] + col * self.cell_size, self.board_boundary_size[1] + row * self.cell_size
        #         x1, y1 = x0 + self.cell_size-1, y0 + self.cell_size-1
        #         self.board.create_rectangle(x0, y0, x1, y1, outline="black", width = 1)

        #         # add text to rectangle
        #         self.board.create_text(x0 + self.cell_size//2, y0 + self.cell_size//2, text=f"({row, col})", font=("Arial", 16), fill="black")


    # def create_player(self):
    #     d = super().create_player()

    #     # add pokemon type to player
    #     dice_roll = self.roll_dice()
    #     d["type"] = "water" if dice_roll <= 2 else "fire" if dice_roll <= 4 else "grass"

    #     # calculate values for the player board
    #     player_id = len(self.players)
    #     r = self.token_size // 2
    #     c1, c2 = r + 5, 2*(r+5)*(player_id+1)

    #     # add pokemon  next to player name
    #     img = Image.open(f"alternative_boardgames/pokemon/assets/{d['type']}-type.png")
    #     img = img.resize((self.token_size, self.token_size))
    #     self.player_types.append(ImageTk.PhotoImage(img))
    #     self.player_board.create_image(200-self.token_size, c2-r, image=self.player_types[player_id], anchor=tk.NW)


        # return d
    
    def take_turn(self):
        dice_roll = self.roll_dice()

        if self.turn_no == 0:
            self.set_player_type(self.player_turn, "water" if dice_roll <= 2 else "fire" if dice_roll <= 4 else "grass")

            # player_id = self.player_turn
            # self.players[player_id]["type"] = "water" if dice_roll <= 2 else "fire" if dice_roll <= 4 else "grass"

            # r = self.token_size // 2
            # c1, c2 = r + 5, 2*(r+5)*(player_id+1)

            # # add pokemon  next to player name
            # img = Image.open(f"alternative_boardgames/pokemon/assets/{self.players[player_id]['type']}-type.png")
            # img = img.resize((self.token_size, self.token_size))
            # self.player_types.append(ImageTk.PhotoImage(img))
            # self.player_board.create_image(200-self.token_size, c2-r, image=self.player_types[player_id], anchor=tk.NW)

            # # move to next player
            # self.player_turn = (self.player_turn + 1) % len(self.players)
            # self.draw_turn_marker()
        else:
             self.move_player(dice_roll, self.player_turn)

        # Take care of battles
        self.battle(self.player_turn)

        # Take care of events
        self.event(self.player_turn)

        # Update the player turn
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.draw_turn_marker()
        
        # Update the turn number
        if self.player_turn == 0:
            self.turn_no += 1

    def battle(self, player_id):
        pass

    def event(self, player_id):
        pos = self.players[player_id]["position"]

        if pos == 4:
            self.set_player_type(player_id, "electric")


    def set_player_type(self, player_id, player_type):
        player_id = self.player_turn

        if self.players[player_id].get("type_token", None) is not None:
            self.player_board.delete(self.players[player_id]["type_token"])

        self.players[player_id]["type"] = player_type

        r = self.token_size // 2
        c1, c2 = r + 5, 2*(r+5)*(player_id+1)

        # add pokemon  next to player name
        
        self.players[player_id]["type_token"] = self.player_board.create_image(200-self.token_size, c2-r, image=self.player_type_tokens[player_type], anchor=tk.NW)

if __name__ == "__main__":
    game = Pokemon(num_players=3)
    # game = BoardGame(board_size = (9,9), cell_size = None, board_boundary_ratio = 259/(449-259))
    game.mainloop()