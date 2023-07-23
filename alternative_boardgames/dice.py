import tkinter as tk
import random
import time


class Dice:

    number = ['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    max_intermediate_frames = 3
    intermediate_frame_time = 0.2


    def __init__(self, tk_window, sides = 6) -> None:
        self.sides = sides
        self.tk_window = tk_window

        # self.roll()
        self.value = 0
        self.draw()

    def roll(self):
        self.value = 0

        for _ in range(self.max_intermediate_frames):
            
            self.value = random.randint(1,self.sides)
            self.draw()
            time.sleep(self.intermediate_frame_time)

    
    def draw(self):
        self.token = tk.Label(self.tk_window,font=('bold',400))

        if self.value == 0:
            self.token.config(text=f'Roll')
        else:
            self.token.config(text=f'{self.number[self.value-1]}')
        self.token.pack()




if __name__ == "__main__":
    window = tk.Tk()

    dice = Dice(window)
    dice.roll()

    window.mainloop()