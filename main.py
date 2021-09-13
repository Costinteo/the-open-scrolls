from src.game import *


if __name__ == "__main__":
    nirn = Game.getInstance()
    while True:
        nirn.update()
