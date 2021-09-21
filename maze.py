from random import randint
from constants import *


def get_maze(grid):
    walls = dict()
    dead_ends = set()
    # first, have walls around all cells
    for cell in grid.keys():
        walls[cell] = [UP, DOWN, LEFT, RIGHT]
    # now, remove walls to create the maze. Algorithm from https://en.wikipedia.org/wiki/Maze_generation_algorithm
    stack = []
    visited = set()
    visited.add((0, 0))
    stack.append((0, 0))
    not_at_dead_end = True
    while len(stack) > 0:
        current_cell = stack.pop()
        neighbours = get_unvisited_neighbours(current_cell, visited, grid.keys())
        if len(neighbours) > 0:
            not_at_dead_end = True
            stack.append(current_cell)
            index = randint(0, len(neighbours) - 1)
            chosen_neighbour = neighbours[index]
            remove_wall(current_cell, chosen_neighbour, walls)
            visited.add(chosen_neighbour)
            stack.append(chosen_neighbour)
        elif not_at_dead_end:
            # this is a dead end
            dead_ends.add(current_cell)
            not_at_dead_end = False
    # now, find the furthest dead end and make it the end
    highest_dist = 0
    end_cell = (0, 0)
    for end in dead_ends:
        total_dist = end[0] + end[1]
        if highest_dist < total_dist:
            highest_dist = total_dist
            end_cell = end
    return walls, end_cell


def get_xy_from_coordinates(coordinates, grid):
    if coordinates in grid.keys():
        return grid[coordinates]
    else:
        return 0


def remove_wall(current_cell, chosen_cell, walls):
    if current_cell[0] == chosen_cell[0]:
        # the cells have the same x, they are above or below each other
        if current_cell[1] + 1 == chosen_cell[1]:
            # the chosen cell is below the current one. Remove the upper wall from the chosen cell,
            # and the lower one from the current.
            walls[chosen_cell].remove(UP)
            walls[current_cell].remove(DOWN)
        else:
            # the chosen cell is above the current one. Remove the lower wall from the chosen cell,
            # and the upper one from the current.
            walls[chosen_cell].remove(DOWN)
            walls[current_cell].remove(UP)
    else:
        # the cells have the same y, they are to the left or right of each other
        if current_cell[0] + 1 == chosen_cell[0]:
            # the chosen cell is to the right of the current one. Remove the left wall from the chosen cell,
            # and the right one from the current.
            walls[chosen_cell].remove(LEFT)
            walls[current_cell].remove(RIGHT)
        else:
            # the chosen cell is to the left of the current one. Remove the right wall from the chosen cell,
            # and the left one from the current.
            walls[chosen_cell].remove(RIGHT)
            walls[current_cell].remove(LEFT)


def generate_coordinates():
    grid_to_xy = dict()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            grid_to_xy[(x, y)] = (x * WIDTH // GRID_WIDTH, y * HEIGHT // GRID_HEIGHT)
    return grid_to_xy


def get_unvisited_neighbours(cell, visited, allowed_cells):
    neighbours = []
    neighbour = (cell[0] - 1, cell[1])
    if neighbour not in visited and neighbour in allowed_cells:
        neighbours.append(neighbour)
    neighbour = (cell[0] + 1, cell[1])
    if neighbour not in visited and neighbour in allowed_cells:
        neighbours.append(neighbour)
    neighbour = (cell[0], cell[1] - 1)
    if neighbour not in visited and neighbour in allowed_cells:
        neighbours.append(neighbour)
    neighbour = (cell[0], cell[1] + 1)
    if neighbour not in visited and neighbour in allowed_cells:
        neighbours.append(neighbour)
    return neighbours