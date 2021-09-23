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


def get_seconds_since_maze_start(start_time):
    return pygame.time.get_ticks() // 1000 - start_time // 1000


def draw_window(fps_string, buddy_rect, grid, walls, end, completed_maze, game_completion_string, start_time,
                lives_remaining, allowed_time, text_to_show):
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

    if not completed_maze:
        timer_text = TEXT_FONT.render("Time: " + str(allowed_time - get_seconds_since_maze_start(start_time)), True,
                                      WHITE)
        WIN.blit(timer_text, (WIDTH - timer_text.get_width() - 10, HEIGHT - timer_text.get_height() - 10))

    if lives_remaining > 0:
        lives_text = TEXT_FONT.render("Lives: " + str(lives_remaining), True, WHITE)
        WIN.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

    key_to_remove = []
    for time_tuple in text_to_show:
        right_now = pygame.time.get_ticks()
        if time_tuple[0] <= right_now and time_tuple[1] >= right_now:
            # display the text
            text_render = TEXT_FONT.render(text_to_show[time_tuple][1], True, text_to_show[time_tuple][0])
            WIN.blit(text_render, (WIDTH // 2 - text_render.get_width() // 2,
                                   HEIGHT // 2 - text_render.get_height() // 2))
        elif time_tuple[1] <= right_now:
            # this is in the past
            key_to_remove.append(time_tuple)
    for key in key_to_remove:
        del text_to_show[key]

    # if completed_maze and game_completion_string == '':
    #    winner_text = TEXT_FONT.render("YOU DID IT YAY!!", True, GREEN)
    #    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))

    if game_completion_string != '':
        complete_text = TEXT_FONT.render(game_completion_string, True, GREEN)
        WIN.blit(complete_text,
                 (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 2 - complete_text.get_height() // 2))

    pygame.display.update()


def add_item_to_text_to_show(text_to_show, text, colour, start_time, end_time):
    text_to_show[(start_time, end_time)] = (colour, text)


def handle_movement(event, buddy_rect, current_grid_coordinates, grid, walls, text_to_show):
    if len(text_to_show) > 0:
        # do not move while text is being displayed
        return current_grid_coordinates
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
    restart = False
    clock = pygame.time.Clock()
    run = True
    frames = 0
    time_ms = 0
    frames_string = ''
    location_grid = generate_coordinates()
    buddy_rect = pygame.Rect(location_grid[(GRID_WIDTH // 2, GRID_HEIGHT // 2)], (BUDDY_WIDTH, BUDDY_HEIGHT))
    current_grid_coordinates = STARTING_COORDINATES
    mazes = dict()
    game_begin_time = pygame.time.get_ticks()  # the time that the game actually began
    start_time = pygame.time.get_ticks()  # the time that the maze we're on began
    remaining_lives = TOTAL_LIVES
    for i in range(NUMBER_OF_MAZES):
        mazes[i] = get_maze(location_grid)
    # walls, end = get_maze(location_grid)
    current_maze_index = 0
    current_maze = mazes[current_maze_index]
    completed_maze = False  # whether or not the current maze is complete
    time_completed_maze = 0  # time in ms that the end tile was reached
    text_to_show = dict()  # structured like { (TIME_TO_START_SHOWING, TIME_TO_STOP_SHOWING):(COLOR, 'text')) }
    game_completion_string = ''
    allowed_time = SECONDS_PER_MAZE
    while run or len(text_to_show) > 0:
        clock.tick(FPS)
        if len(text_to_show) > 0:
            # pause the timer by making the start time now until we have shown all our text
            start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            # handle events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if not completed_maze:
                    current_grid_coordinates = handle_movement(event, buddy_rect, current_grid_coordinates,
                                                               location_grid, current_maze[0], text_to_show)
                if current_grid_coordinates == current_maze[1]:
                    completed_maze = True
                    time_completed_maze = pygame.time.get_ticks()
                    right_now = pygame.time.get_ticks()
                    add_item_to_text_to_show(text_to_show, 'Maze Complete!', GREEN, right_now, right_now + 3000)

        draw_window(frames_string, buddy_rect, location_grid, current_maze[0], current_maze[1], completed_maze,
                    game_completion_string, start_time, remaining_lives, allowed_time, text_to_show)

        # if they have completed the mze, wait for three seconds, and then move them to the next one, if there is one
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
            allowed_time = SECONDS_PER_MAZE
            right_now = pygame.time.get_ticks()
            add_item_to_text_to_show(text_to_show, 'New Maze!', WHITE, right_now, right_now + 1000)
            add_item_to_text_to_show(text_to_show, '3', WHITE, right_now + 1000, right_now + 2000)
            add_item_to_text_to_show(text_to_show, '2', WHITE, right_now + 2000, right_now + 3000)
            add_item_to_text_to_show(text_to_show, '1', WHITE, right_now + 3000, right_now + 4000)

        if get_seconds_since_maze_start(start_time) > allowed_time:
            # they ran out of time. They need to be reset.
            right_now = pygame.time.get_ticks()
            add_item_to_text_to_show(text_to_show, 'Time Up!', WHITE, right_now, right_now + 2000)
            timer_change_string = 'Time Increase - ' + str(allowed_time) + '->' + str(allowed_time + 7)
            add_item_to_text_to_show(text_to_show, timer_change_string, WHITE, right_now + 2000, right_now + 2500)
            add_item_to_text_to_show(text_to_show, '', WHITE, right_now + 2500, right_now + 3000)
            add_item_to_text_to_show(text_to_show, timer_change_string, WHITE, right_now + 3000, right_now + 3500)
            add_item_to_text_to_show(text_to_show, '', WHITE, right_now + 3500, right_now + 4000)
            add_item_to_text_to_show(text_to_show, timer_change_string, WHITE, right_now + 4000, right_now + 4500)
            add_item_to_text_to_show(text_to_show, 'Lives: ' + str(remaining_lives), WHITE, right_now + 4500,
                                     right_now + 5500)
            remaining_lives -= 1
            if remaining_lives < 0:
                run = False
                restart = True
                add_item_to_text_to_show(text_to_show, 'Game Over! Restarting game...', WHITE, right_now + 5500,
                                         right_now + 8500)
            else:
                add_item_to_text_to_show(text_to_show, 'Lives: ' + str(remaining_lives), WHITE, right_now + 5500,
                                         right_now + 6500)
                add_item_to_text_to_show(text_to_show, '3', WHITE, right_now + 6500, right_now + 7500)
                add_item_to_text_to_show(text_to_show, '2', WHITE, right_now + 7500, right_now + 8500)
                add_item_to_text_to_show(text_to_show, '1', WHITE, right_now + 8500, right_now + 9500)
                current_grid_coordinates = STARTING_COORDINATES
                xy = get_xy_from_coordinates(current_grid_coordinates, location_grid)
                buddy_rect.x = xy[0]
                buddy_rect.y = xy[1]
                start_time = pygame.time.get_ticks()
                allowed_time += 7

        # if they completed the final maze
        if completed_maze and current_maze_index == 6:
            # completed game
            game_completion_string = "CONGRATULATIONS!\n"
            game_completion_string += "Time: " + str((pygame.time.get_ticks() - game_begin_time) // 1000)
            current_maze_index += 1

        frames += 1
        current_time_ms = pygame.time.get_ticks() % 1000
        if time_ms > current_time_ms:
            frames_string = repr(frames)
            frames = 0
        time_ms = current_time_ms
    if restart:
        game()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game()
