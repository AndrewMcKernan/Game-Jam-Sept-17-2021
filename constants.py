WIDTH, HEIGHT = 777, 777  # dimensions of screen

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3 # directional codes for walls

GRID_WIDTH, GRID_HEIGHT = 11, 11
BUDDY_WIDTH, BUDDY_HEIGHT = WIDTH // GRID_WIDTH - WIDTH // GRID_WIDTH // 9, HEIGHT // GRID_HEIGHT - HEIGHT // GRID_HEIGHT // 9

WALL_WIDTH = WIDTH // GRID_WIDTH
WALL_HEIGHT = HEIGHT // GRID_HEIGHT

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
IDK = (120, 240, 90)

FPS = 60  # more needs to be done here when frames are dropped - at this point, it will simply slow down the game.
