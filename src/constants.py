# Screen Size and others
WIDTH, HEIGHT = 1280, 720
PADDING = 60
FPS = 60

# Colours and aesthetics
BACKGROUNDCOLOUR = (255, 255, 255)
WALLSCOLOUR = (0, 0, 0)
PLAYERCOLOUR = (0, 255, 0)
ENEMYCOLOUR = (255, 0, 0)
NAVY = (10, 10, 80)
FONT = "dejavusans"


# Game related
# unused
MAX_ATTRIBUTES = 3

# class used to draw levels and entities
# its static variables are updated when a level is loaded
class DrawInfo():

    ROWS = 0
    COLS = 0
    X_OFFSET = 0
    Y_OFFSET = 0

    CELL_WIDTH = 0
    CELL_HEIGHT = 0

    ENTITY_WIDTH = 0
    ENTITY_HEIGHT = 0