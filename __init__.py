"""
Evan's Tomb
Written by Evan Prael, May 2024

Based on a tile puzzle in the game "Lego Indiana Jones: The Original Adventures"

Sample video of the original puzzle:
https://www.youtube.com/watch?v=zsoePC73dnE

Sample video of this game:
https://www.youtube.com/watch?v=OR1Nz0TAC08

This is the main entry point for the game. It creates the game loop and
starts the game.

"""


from game_loop import GameLoop

if __name__ == "__main__":
    game = GameLoop()
    game.run()
