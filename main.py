import pygame, os

pygame.font.init()  # for writing text to the screen
pygame.mixer.init()  # for sound

WIDTH, HEIGHT = 900, 900  # dimensions of screen

GRID_WIDTH, GRID_HEIGHT = 10, 10
BUDDY_WIDTH, BUDDY_HEIGHT = WIDTH // GRID_WIDTH - WIDTH // GRID_WIDTH // 9, HEIGHT // GRID_HEIGHT - HEIGHT // GRID_HEIGHT // 9
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beginner Jam - Sept 17, 2021")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)

# VERTICAL_GRID_LINE = pygame.Rect()

BUDDY_IMAGE = pygame.image.load(os.path.join('assets', 'buddy.png')).convert()
BARRIER_IMAGE = pygame.image.load(os.path.join('assets', 'barrier.png')).convert()

BUDDY = pygame.transform.scale(BUDDY_IMAGE, (BUDDY_WIDTH, BUDDY_HEIGHT))

BARRIER = pygame.transform.scale(BARRIER_IMAGE, (BUDDY_WIDTH, BUDDY_HEIGHT))

TEXT_FONT = pygame.font.SysFont('lucidaconsole', 40)

FPS = 60  # more needs to be done here when frames are dropped - at this point, it will simply slow down the game.


def draw_window(fps_string, buddy_rect, grid, barriers):
    pygame.draw.rect(WIN, BLACK, BACKGROUND)

    # draw gridlines
    for x in range(GRID_WIDTH):
        line = pygame.Rect(grid[x, 0], (1, HEIGHT))
        pygame.draw.rect(WIN, WHITE, line)
    for y in range(GRID_HEIGHT):
        line = pygame.Rect(grid[0, y], (WIDTH, 1))
        pygame.draw.rect(WIN, WHITE, line)

    for barrier in barriers:
        xy = grid[barrier]
        WIN.blit(BARRIER, (xy[0] + WIDTH // GRID_WIDTH // 18, xy[1] + HEIGHT // GRID_HEIGHT // 18))

    WIN.blit(BUDDY, (buddy_rect.x + WIDTH // GRID_WIDTH // 18, buddy_rect.y + HEIGHT // GRID_HEIGHT // 18))

    fps_text = TEXT_FONT.render(fps_string, True, WHITE)
    WIN.blit(fps_text, (10, 10))
    pygame.display.update()


def generate_coordinates():
    grid_to_xy = dict()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            grid_to_xy[(x, y)] = (x * WIDTH // GRID_WIDTH, y * HEIGHT // GRID_HEIGHT)
    return grid_to_xy


def get_xy_from_coordinates(coordinates, grid):
    if coordinates in grid.keys():
        return grid[coordinates]
    else:
        return 0


def handle_movement(event, buddy_rect, current_grid_coordinates, grid, barriers):
    if event.key == pygame.K_w:
        moved_coordinates = (current_grid_coordinates[0], current_grid_coordinates[1] - 1)
        if moved_coordinates in barriers:
            return current_grid_coordinates
        xy = get_xy_from_coordinates(moved_coordinates, grid)
        if xy != 0:
            buddy_rect.y = xy[1]
            return moved_coordinates
    elif event.key == pygame.K_s:
        moved_coordinates = (current_grid_coordinates[0], current_grid_coordinates[1] + 1)
        if moved_coordinates in barriers:
            return current_grid_coordinates
        xy = get_xy_from_coordinates(moved_coordinates, grid)
        if xy != 0:
            buddy_rect.y = xy[1]
            return moved_coordinates
    elif event.key == pygame.K_a:
        moved_coordinates = (current_grid_coordinates[0] - 1, current_grid_coordinates[1])
        if moved_coordinates in barriers:
            return current_grid_coordinates
        xy = get_xy_from_coordinates(moved_coordinates, grid)
        if xy != 0:
            buddy_rect.x = xy[0]
            return moved_coordinates
    elif event.key == pygame.K_d:
        moved_coordinates = (current_grid_coordinates[0] + 1, current_grid_coordinates[1])
        if moved_coordinates in barriers:
            return current_grid_coordinates
        xy = get_xy_from_coordinates(moved_coordinates, grid)
        if xy != 0:
            buddy_rect.x = xy[0]
            return moved_coordinates
    return current_grid_coordinates


def game():
    clock = pygame.time.Clock()
    run = True
    frames = 0
    time_ms = 0
    frames_string = ''
    location_grid = generate_coordinates()
    buddy_rect = pygame.Rect(location_grid[(0, 0)], (BUDDY_WIDTH, BUDDY_HEIGHT))
    current_grid_coordinates = (0, 0)
    #barriers = []
    barriers = [(5, 0), (5, 1), (5, 2), (0, 2), (1, 2), (2, 2), (3, 2), (6, 2), (7, 2), (8, 2), (5, 4), (6, 4), (7, 4),
                (8, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 5), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (0, 7),
                (1, 7), (2, 7), (3, 7), (5, 7), (3, 8), (5, 8), (7, 8), (3, 9), (7, 9)]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # handle events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                current_grid_coordinates = handle_movement(event, buddy_rect, current_grid_coordinates, location_grid,
                                                           barriers)

        draw_window(frames_string, buddy_rect, location_grid, barriers)

        frames += 1
        current_time_ms = pygame.time.get_ticks() % 1000
        if time_ms > current_time_ms:
            frames_string = repr(frames)
            frames = 0
        time_ms = current_time_ms


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game()
