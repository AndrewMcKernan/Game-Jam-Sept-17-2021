WIDTH, HEIGHT = 777, 777  # dimensions of screen

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3  # directional codes for walls

NUMBER_OF_MAZES = 7

GRID_WIDTH, GRID_HEIGHT = 16, 16
BUDDY_WIDTH, BUDDY_HEIGHT = WIDTH // GRID_WIDTH - WIDTH // GRID_WIDTH // 9, HEIGHT // GRID_HEIGHT - HEIGHT // GRID_HEIGHT // 9

WALL_WIDTH = WIDTH // GRID_WIDTH
WALL_HEIGHT = HEIGHT // GRID_HEIGHT

ZOOM_FACTOR = 4

ZOOMED_MAZE_WIDTH = WIDTH * ZOOM_FACTOR
ZOOMED_MAZE_HEIGHT = HEIGHT * ZOOM_FACTOR

#ZOOMED_GRID_WIDTH = GRID_WIDTH // ZOOM_FACTOR
#ZOOMED_GRID_HEIGHT = GRID_HEIGHT // ZOOM_FACTOR

ZOOMED_WALL_WIDTH = WALL_WIDTH * ZOOM_FACTOR
ZOOMED_WALL_HEIGHT = WALL_HEIGHT * ZOOM_FACTOR

ZOOMED_BUDDY_WIDTH = BUDDY_WIDTH * ZOOM_FACTOR
ZOOMED_BUDDY_HEIGHT = BUDDY_HEIGHT * ZOOM_FACTOR

STARTING_COORDINATES = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
IDK = (120, 240, 90)

FPS = 60  # more needs to be done here when frames are dropped - at this point, it will simply slow down the game.

SECONDS_PER_MAZE = 17

TOTAL_LIVES = 7
