# Legacy main.py - redirects to new modular game structure
# Run this file to play the refactored Space Invaders

from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()