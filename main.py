import os
import pygame
from maze import *
from constants import *
from draw_text import drawText

pygame.font.init()  # for writing text to the screen
pygame.mixer.init()  # for sound

pygame.display.set_caption("Beginner Jam - Sept 17, 2021")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

ZOOMED_MAZE = pygame.surface.Surface((ZOOMED_MAZE_WIDTH, ZOOMED_MAZE_HEIGHT))
camera = pygame.Rect((ZOOMED_MAZE_WIDTH // 2 - WIDTH // 2, ZOOMED_MAZE_HEIGHT // 2 - HEIGHT // 2), (WIDTH, HEIGHT))

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)
ZOOMED_BACKGROUND = pygame.Rect(0, 0, ZOOMED_MAZE_WIDTH, ZOOMED_MAZE_HEIGHT)

BUDDY_IMAGE = pygame.image.load(os.path.join('assets', 'buddy.png')).convert()
BARRIER_IMAGE = pygame.image.load(os.path.join('assets', 'barrier.png')).convert()

pygame.mixer.music.load(os.path.join('assets', 'Spy.mp3'))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

BUDDY = pygame.transform.scale(BUDDY_IMAGE, (BUDDY_WIDTH, BUDDY_HEIGHT))
ZOOMED_BUDDY = pygame.transform.scale(BUDDY_IMAGE, (ZOOMED_BUDDY_WIDTH, ZOOMED_BUDDY_HEIGHT))

BARRIER = pygame.transform.scale(BARRIER_IMAGE, (BUDDY_WIDTH, BUDDY_HEIGHT))

TEXT_FONT = pygame.font.SysFont('lucidaconsole', 40)
DESC_FONT = pygame.font.SysFont('lucidaconsole', 20)
CELL_FONT = pygame.font.SysFont('lucidaconsole', 10)


def get_seconds_since_maze_start(start_time):
    return pygame.time.get_ticks() // 1000 - start_time // 1000


def draw_title():
    pygame.draw.rect(WIN, BLACK, BACKGROUND)
    title_text = TEXT_FONT.render('Septopus', True, WHITE)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))
    desc_1 = 'You are the septopus, an illegal government clone of the almighty octopus - with only 7 tentacles!'
    rect_1 = pygame.Rect(0, title_text.get_height() + 55, WIDTH, HEIGHT // 7)
    drawText(WIN, desc_1, WHITE, rect_1, DESC_FONT, True)
    desc_2 = 'You need to escape this research facility and reclaim your life in the open ocean.'
    rect_2 = pygame.Rect(0, title_text.get_height() + 55 + HEIGHT // 7, WIDTH, HEIGHT // 7)
    drawText(WIN, desc_2, WHITE, rect_2, DESC_FONT, True)
    desc_3 = 'To do so, you need to navigate 7 mazes before the automatic locks close in each maze!'
    rect_3 = pygame.Rect(0, title_text.get_height() + 55 + 2 * HEIGHT // 7, WIDTH, HEIGHT // 7)
    drawText(WIN, desc_3, WHITE, rect_3, DESC_FONT, True)
    desc_4 = "If you fail, don't worry. You have the power to reset time 7 times - once per tentacle."
    rect_4 = pygame.Rect(0, title_text.get_height() + 55 + 3 * HEIGHT // 7, WIDTH, HEIGHT // 7)
    drawText(WIN, desc_4, WHITE, rect_4, DESC_FONT, True)
    desc_5 = "Before you start, be sure to memorize the maze's layout as best you can. Once you start moving, your vision will be reduced!"
    rect_5 = pygame.Rect(0, title_text.get_height() + 55 + 4 * HEIGHT // 7, WIDTH, HEIGHT // 7)
    drawText(WIN, desc_5, WHITE, rect_5, DESC_FONT, True)
    desc_6 = "Good luck! Press ENTER to begin."
    rect_6 = pygame.Rect(0, title_text.get_height() + 55 + 5 * HEIGHT // 7, WIDTH, HEIGHT // 7)
    drawText(WIN, desc_6, WHITE, rect_6, DESC_FONT, True)

    desc_7 = 'Music By Nicole Marie T'
    rect_7 = pygame.Rect(0, title_text.get_height() + 35 + 6 * HEIGHT // 7, WIDTH, HEIGHT // 7)
    drawText(WIN, desc_7, WHITE, rect_7, DESC_FONT, True)

    pygame.display.update()


def draw_window(fps_string, buddy_rect, grid, zoomed_grid, walls, end, completed_maze, start_time, lives_remaining,
                allowed_time, text_to_show, text_needing_acknowledgement, zoomed):
    pygame.draw.rect(WIN, BLACK, BACKGROUND)
    if not zoomed:
        # draw walls
        end_rect = pygame.Rect(get_xy_from_coordinates(end, grid), (WALL_WIDTH, WALL_HEIGHT))
        pygame.draw.rect(WIN, GREEN, end_rect)
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

        # draw character
        WIN.blit(BUDDY, (buddy_rect.x + WIDTH // GRID_WIDTH // 18, buddy_rect.y + HEIGHT // GRID_HEIGHT // 18))
    else:
        pygame.draw.rect(ZOOMED_MAZE, BLACK, ZOOMED_BACKGROUND)
        end_rect = pygame.Rect(get_xy_from_coordinates(end, zoomed_grid), (ZOOMED_WALL_WIDTH, ZOOMED_WALL_HEIGHT))
        pygame.draw.rect(ZOOMED_MAZE, GREEN, end_rect)
        # draw walls
        for cell in walls:
            for wall in walls[cell]:
                if wall == UP:
                    line = pygame.Rect(get_xy_from_coordinates(cell, zoomed_grid), (ZOOMED_WALL_WIDTH, 1))
                    pygame.draw.rect(ZOOMED_MAZE, WHITE, line)
                if wall == DOWN:
                    coords = get_xy_from_coordinates(cell, zoomed_grid)
                    coords = (coords[0], coords[1] + ZOOMED_WALL_HEIGHT)
                    line = pygame.Rect(coords, (ZOOMED_WALL_WIDTH, 1))
                    pygame.draw.rect(ZOOMED_MAZE, WHITE, line)
                if wall == LEFT:
                    line = pygame.Rect(get_xy_from_coordinates(cell, zoomed_grid), (1, ZOOMED_WALL_HEIGHT))
                    pygame.draw.rect(ZOOMED_MAZE, RED, line)
                if wall == RIGHT:
                    coords = get_xy_from_coordinates(cell, zoomed_grid)
                    coords = (coords[0] + ZOOMED_WALL_WIDTH, coords[1])
                    line = pygame.Rect(coords, (1, ZOOMED_WALL_HEIGHT))
                    pygame.draw.rect(ZOOMED_MAZE, RED, line)

        # draw character
        ZOOMED_MAZE.blit(ZOOMED_BUDDY, (buddy_rect.x + ZOOMED_MAZE_WIDTH // GRID_WIDTH // 18, buddy_rect.y + ZOOMED_MAZE_HEIGHT // GRID_HEIGHT // 18))
        camera.x = buddy_rect.x + ZOOMED_BUDDY_WIDTH // 2 - WIDTH // 2
        camera.y = buddy_rect.y + ZOOMED_BUDDY_HEIGHT // 2 - HEIGHT // 2
        WIN.blit(ZOOMED_MAZE, (0, 0), camera)

    # draw text
    fps_text = TEXT_FONT.render(fps_string, True, WHITE)
    WIN.blit(fps_text, (10, 10))

    if not completed_maze:
        timer_text = TEXT_FONT.render("Time: " + str(allowed_time - get_seconds_since_maze_start(start_time)), True,
                                      WHITE)
        WIN.blit(timer_text, (WIDTH - timer_text.get_width() - 10, HEIGHT - timer_text.get_height() - 10))

    if lives_remaining > 0:
        lives_text = TEXT_FONT.render("Lives: " + str(lives_remaining), True, WHITE)
        WIN.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

    if len(text_needing_acknowledgement) > 0:
        rect = pygame.Rect(WIDTH // 7, HEIGHT // 2, WIDTH - 2 * WIDTH // 7, HEIGHT // 2)
        drawText(WIN, text_needing_acknowledgement[0][1], text_needing_acknowledgement[0][0], rect, TEXT_FONT)

    key_to_remove = []
    for time_tuple in text_to_show:
        right_now = pygame.time.get_ticks()
        if time_tuple[0] <= right_now <= time_tuple[1]:
            # display the text
            text_render = TEXT_FONT.render(text_to_show[time_tuple][1], True, text_to_show[time_tuple][0])
            WIN.blit(text_render, (WIDTH // 2 - text_render.get_width() // 2,
                                   HEIGHT // 2 - text_render.get_height() // 2))
        elif time_tuple[1] <= right_now:
            # this is in the past
            key_to_remove.append(time_tuple)
    for key in key_to_remove:
        del text_to_show[key]

    pygame.display.update()


def add_item_to_text_to_show(text_to_show, text, colour, start_time, end_time):
    text_to_show[(start_time, end_time)] = (colour, text)


def add_item_to_text_needing_acknowledgement(text_needing_acknowledgement, text, colour):
    text_needing_acknowledgement.append((colour, text))


def handle_animation(buddy_rect, next_buddy_xy):
    if len(next_buddy_xy) > 0:
        # set the xy of the buddy to the next one and get rid of it
        buddy_rect.x = next_buddy_xy[0][0]
        buddy_rect.y = next_buddy_xy[0][1]
        del next_buddy_xy[0]


def handle_movement(event, buddy_rect, current_grid_coordinates, grid, zoomed_grid, walls, text_to_show, zoomed,
                    next_buddy_xy):
    if len(text_to_show) > 0:
        # do not move while text is being displayed
        return current_grid_coordinates
    if len(next_buddy_xy) > 0:
        # do not allow new inputs when animation not complete
        return current_grid_coordinates
    if event.key == pygame.K_w:
        moved_coordinates = (current_grid_coordinates[0], current_grid_coordinates[1] - 1)
        if UP in walls[current_grid_coordinates]:  # there is a wall above us
            return current_grid_coordinates
        if not zoomed:
            xy = get_xy_from_coordinates(moved_coordinates, grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x, buddy_rect.y - frame * WALL_HEIGHT // FRAMES_PER_MOVE))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.y = buddy_rect.y - GRID_HEIGHT // FRAMES_PER_MOVE
                return moved_coordinates
        else:
            xy = get_xy_from_coordinates(moved_coordinates, zoomed_grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x, buddy_rect.y - frame * ZOOMED_WALL_HEIGHT // FRAMES_PER_MOVE))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.y = buddy_rect.y - ZOOMED_WALL_HEIGHT // FRAMES_PER_MOVE
                return moved_coordinates

    elif event.key == pygame.K_s:
        moved_coordinates = (current_grid_coordinates[0], current_grid_coordinates[1] + 1)
        if DOWN in walls[current_grid_coordinates]:  # there is a wall below us
            return current_grid_coordinates
        if not zoomed:
            xy = get_xy_from_coordinates(moved_coordinates, grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x, buddy_rect.y + frame * WALL_HEIGHT // FRAMES_PER_MOVE))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.y = buddy_rect.y + WALL_HEIGHT // FRAMES_PER_MOVE
                return moved_coordinates
        else:
            xy = get_xy_from_coordinates(moved_coordinates, zoomed_grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x, buddy_rect.y + frame * ZOOMED_WALL_HEIGHT // FRAMES_PER_MOVE))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.y = buddy_rect.y + ZOOMED_WALL_HEIGHT // FRAMES_PER_MOVE
                return moved_coordinates
    elif event.key == pygame.K_a:
        moved_coordinates = (current_grid_coordinates[0] - 1, current_grid_coordinates[1])
        if LEFT in walls[current_grid_coordinates]:  # there is a wall to the left of us
            return current_grid_coordinates
        if not zoomed:
            xy = get_xy_from_coordinates(moved_coordinates, grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x - frame * WALL_WIDTH // FRAMES_PER_MOVE, buddy_rect.y))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.x = buddy_rect.x - WALL_WIDTH // FRAMES_PER_MOVE
                return moved_coordinates
        else:
            xy = get_xy_from_coordinates(moved_coordinates, zoomed_grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x - frame * ZOOMED_WALL_WIDTH // FRAMES_PER_MOVE, buddy_rect.y))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.x = buddy_rect.x - ZOOMED_WALL_WIDTH // FRAMES_PER_MOVE
                return moved_coordinates
    elif event.key == pygame.K_d:
        moved_coordinates = (current_grid_coordinates[0] + 1, current_grid_coordinates[1])
        if RIGHT in walls[current_grid_coordinates]:  # there is a wall to the right of us
            return current_grid_coordinates
        if not zoomed:
            xy = get_xy_from_coordinates(moved_coordinates, grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x + frame * WALL_WIDTH // FRAMES_PER_MOVE, buddy_rect.y))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.x = buddy_rect.x + WALL_WIDTH // FRAMES_PER_MOVE
                return moved_coordinates
        else:
            xy = get_xy_from_coordinates(moved_coordinates, zoomed_grid)
            frame = 2
            while frame < FRAMES_PER_MOVE:
                next_buddy_xy.append((buddy_rect.x + frame * ZOOMED_WALL_WIDTH // FRAMES_PER_MOVE, buddy_rect.y))
                frame += 1
            next_buddy_xy.append((xy[0], xy[1]))
            if xy != 0:
                buddy_rect.x = buddy_rect.x + ZOOMED_WALL_WIDTH // FRAMES_PER_MOVE
                return moved_coordinates
    return current_grid_coordinates


def game():
    restart = False
    clock = pygame.time.Clock()
    title_mode = True
    run = True
    zoomed = False
    frames = 0
    time_ms = 0
    frames_string = ''
    location_grid = generate_coordinates()
    zoomed_location_grid = generate_zoomed_coordinates()
    buddy_rect = pygame.Rect(location_grid[(GRID_WIDTH // 2, GRID_HEIGHT // 2)], (BUDDY_WIDTH, BUDDY_HEIGHT))
    current_grid_coordinates = STARTING_COORDINATES
    mazes = dict()
    game_begin_time = pygame.time.get_ticks()  # the time that the game actually began
    start_time = pygame.time.get_ticks()  # the time that the maze we're on began
    remaining_lives = TOTAL_LIVES
    next_buddy_xy = []
    for i in range(NUMBER_OF_MAZES):
        mazes[i] = get_maze(location_grid)
    # walls, end = get_maze(location_grid)
    current_maze_index = 0
    current_maze = mazes[current_maze_index]
    completed_maze = False  # whether or not the current maze is complete
    time_completed_maze = 0  # time in ms that the end tile was reached
    text_to_show = dict()  # structured like { (TIME_TO_START_SHOWING, TIME_TO_STOP_SHOWING):(COLOR, 'text')) }
    text_needing_acknowledgement = []  # structured like [ (COLOR, 'text')) ]
    allowed_time = SECONDS_PER_MAZE

    while title_mode:
        draw_title()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                title_mode = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    title_mode = False
                    add_item_to_text_needing_acknowledgement(text_needing_acknowledgement, 'Press any button to start!',
                                                             WHITE)

    while run or len(text_to_show) > 0 or len(text_needing_acknowledgement) > 0:
        clock.tick(FPS)
        handle_animation(buddy_rect, next_buddy_xy)
        if len(text_to_show) > 0 or len(text_needing_acknowledgement):
            # pause the timer by making the start time now until we have shown all our text
            start_time = pygame.time.get_ticks()
            # while there is text on the screen, show the whole map
            zoomed = False
        elif len(next_buddy_xy) < 1:
            # zoom in when all the text is gone
            zoomed = True
            xy = get_xy_from_coordinates(current_grid_coordinates, zoomed_location_grid)
            buddy_rect.x = xy[0]
            buddy_rect.y = xy[1]
        for event in pygame.event.get():
            # handle events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                continue
            if event.type == pygame.KEYDOWN:
                if len(text_needing_acknowledgement) > 0:
                    del text_needing_acknowledgement[0]
                    if run:
                        right_now = pygame.time.get_ticks()
                        add_item_to_text_to_show(text_to_show, '3', WHITE, right_now + 1000, right_now + 2000)
                        add_item_to_text_to_show(text_to_show, '2', WHITE, right_now + 2000, right_now + 3000)
                        add_item_to_text_to_show(text_to_show, '1', WHITE, right_now + 3000, right_now + 4000)
                else:
                    if not completed_maze:
                        current_grid_coordinates = handle_movement(event, buddy_rect, current_grid_coordinates,
                                                                   location_grid, zoomed_location_grid, current_maze[0],
                                                                   text_to_show, zoomed, next_buddy_xy)
                    if current_grid_coordinates == current_maze[1]:
                        completed_maze = True
                        time_completed_maze = pygame.time.get_ticks()
                        right_now = pygame.time.get_ticks()
                        if current_maze_index < 6:
                            add_item_to_text_to_show(text_to_show, 'Maze Complete!', GREEN, right_now, right_now + 3000)

        draw_window(frames_string, buddy_rect, location_grid, zoomed_location_grid, current_maze[0], current_maze[1], completed_maze,
                    start_time, remaining_lives, allowed_time, text_to_show,
                    text_needing_acknowledgement, zoomed)

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
            add_item_to_text_needing_acknowledgement(text_needing_acknowledgement,
                                                     'New Maze! Press any button to start.', WHITE)

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
            game_completion_string = "CONGRATULATIONS! "
            game_completion_string += "Time: " + str((pygame.time.get_ticks() - game_begin_time) // 1000)
            add_item_to_text_needing_acknowledgement(text_needing_acknowledgement, game_completion_string, GREEN)
            current_maze_index += 1
            run = False
            restart = True

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
