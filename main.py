import os
import pygame
from maze import *
from constants import *

pygame.font.init()  # for writing text to the screen
pygame.mixer.init()  # for sound

pygame.display.set_caption("Beginner Jam - Sept 17, 2021")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)

BUDDY_IMAGE = pygame.image.load(os.path.join('assets', 'buddy.png')).convert()
BARRIER_IMAGE = pygame.image.load(os.path.join('assets', 'barrier.png')).convert()

BUDDY = pygame.transform.scale(BUDDY_IMAGE, (BUDDY_WIDTH, BUDDY_HEIGHT))

BARRIER = pygame.transform.scale(BARRIER_IMAGE, (BUDDY_WIDTH, BUDDY_HEIGHT))

TEXT_FONT = pygame.font.SysFont('lucidaconsole', 40)
CELL_FONT = pygame.font.SysFont('lucidaconsole', 10)


def draw_window(fps_string, buddy_rect, grid, walls, end, completed_maze, game_completion_string, start_time):
    pygame.draw.rect(WIN, BLACK, BACKGROUND)
    end_rect = pygame.Rect(get_xy_from_coordinates(end, grid), (WALL_WIDTH, WALL_HEIGHT))
    pygame.draw.rect(WIN, GREEN, end_rect)

    # draw walls
    for cell in walls:
        for wall in walls[cell]:
            if wall == UP:
                line = pygame.Rect(get_xy_from_coordinates(cell, grid), (WALL_WIDTH, 1))
                pygame.draw.rect(WIN, WHITE, line)
            if wall == DOWN:
                coords = get_xy_from_coordinates(cell, grid)
                coords = (coords[0], coords[1] + WALL_HEIGHT)
                line = pygame.Rect(coords, (WALL_WIDTH, 1))
                pygame.draw.rect(WIN, WHITE, line)
            if wall == LEFT:
                line = pygame.Rect(get_xy_from_coordinates(cell, grid), (1, WALL_HEIGHT))
                pygame.draw.rect(WIN, RED, line)
            if wall == RIGHT:
                coords = get_xy_from_coordinates(cell, grid)
                coords = (coords[0] + WALL_WIDTH, coords[1])
                line = pygame.Rect(coords, (1, WALL_HEIGHT))
                pygame.draw.rect(WIN, RED, line)

    WIN.blit(BUDDY, (buddy_rect.x + WIDTH // GRID_WIDTH // 18, buddy_rect.y + HEIGHT // GRID_HEIGHT // 18))

    fps_text = TEXT_FONT.render(fps_string, True, WHITE)
    WIN.blit(fps_text, (10, 10))

    timer_text = TEXT_FONT.render(str(SECONDS_PER_MAZE - (pygame.time.get_ticks() // 1000 - start_time // 1000)), True, WHITE)
    WIN.blit(timer_text, (WIDTH - timer_text.get_width() - 10, HEIGHT - timer_text.get_height() - 10))

    if completed_maze and game_completion_string == '':
        winner_text = TEXT_FONT.render("YOU DID IT YAY!!", True, GREEN)
        WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))

    if game_completion_string != '':
        complete_text = TEXT_FONT.render(game_completion_string, True, GREEN)
        WIN.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 2 - complete_text.get_height() // 2))

    pygame.display.update()


def handle_movement(event, buddy_rect, current_grid_coordinates, grid, walls):
    if event.key == pygame.K_w:
        moved_coordinates = (current_grid_coordinates[0], current_grid_coordinates[1] - 1)
        if UP in walls[current_grid_coordinates]:  # there is a wall above us
            return current_grid_coordinates
        xy = get_xy_from_coordinates(moved_coordinates, grid)
        if xy != 0:
            buddy_rect.y = xy[1]
            return moved_coordinates
    elif event.key == pygame.K_s:
        moved_coordinates = (current_grid_coordinates[0], current_grid_coordinates[1] + 1)
        if DOWN in walls[current_grid_coordinates]:  # there is a wall below us
            return current_grid_coordinates
        xy = get_xy_from_coordinates(moved_coordinates, grid)
        if xy != 0:
            buddy_rect.y = xy[1]
            return moved_coordinates
    elif event.key == pygame.K_a:
        moved_coordinates = (current_grid_coordinates[0] - 1, current_grid_coordinates[1])
        if LEFT in walls[current_grid_coordinates]:  # there is a wall to the left of us
            return current_grid_coordinates
        xy = get_xy_from_coordinates(moved_coordinates, grid)
        if xy != 0:
            buddy_rect.x = xy[0]
            return moved_coordinates
    elif event.key == pygame.K_d:
        moved_coordinates = (current_grid_coordinates[0] + 1, current_grid_coordinates[1])
        if RIGHT in walls[current_grid_coordinates]:  # there is a wall to the right of us
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
    buddy_rect = pygame.Rect(location_grid[(GRID_WIDTH // 2, GRID_HEIGHT // 2)], (BUDDY_WIDTH, BUDDY_HEIGHT))
    current_grid_coordinates = STARTING_COORDINATES
    mazes = dict()
    start_time = pygame.time.get_ticks()
    for i in range(NUMBER_OF_MAZES):
        mazes[i] = get_maze(location_grid)
    # walls, end = get_maze(location_grid)
    current_maze_index = 0
    current_maze = mazes[current_maze_index]
    completed_maze = False
    time_completed_maze = 0
    game_completion_string = ''
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # handle events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if not completed_maze:
                    current_grid_coordinates = handle_movement(event, buddy_rect, current_grid_coordinates,
                                                               location_grid, current_maze[0])
                if current_grid_coordinates == current_maze[1]:
                    completed_maze = True
                    time_completed_maze = pygame.time.get_ticks()

        draw_window(frames_string, buddy_rect, location_grid, current_maze[0], current_maze[1], completed_maze,
                    game_completion_string, start_time)

        if completed_maze and time_completed_maze + 3000 < pygame.time.get_ticks() and current_maze_index < 6:
            # move them to the next maze after 3 seconds
            completed_maze = False
            current_maze_index += 1
            current_maze = mazes[current_maze_index]
            current_grid_coordinates = STARTING_COORDINATES
            xy = get_xy_from_coordinates(current_grid_coordinates, location_grid)
            buddy_rect.x = xy[0]
            buddy_rect.y = xy[1]
            start_time = pygame.time.get_ticks()

        if completed_maze and current_maze_index == 6:
            # completed game
            game_completion_string = "CONGRATULATIONS!\n"
            game_completion_string += "Time: " + str((pygame.time.get_ticks() - start_time) // 1000)
            current_maze_index += 1

        frames += 1
        current_time_ms = pygame.time.get_ticks() % 1000
        if time_ms > current_time_ms:
            frames_string = repr(frames)
            frames = 0
        time_ms = current_time_ms


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game()
