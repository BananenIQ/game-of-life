import pygame as game
import numpy as np
import pygame_gui as gui

RUNNING = True
SIZE_GRID = 75, 75
WIDTH_GRID, HEIGHT_GRID = 20, 20
MARGIN = 1

generation_dict = {}


def run_GameUI(size_grid, w_grid, h_grid, margin, run, grid_array):
    window_size = size_grid[0] * (w_grid + margin), size_grid[1] * (h_grid + margin)
    game.init()
    width, height = window_size
    generation = 0

    game.display.set_caption("Game of Life")
    screen = game.display.set_mode(window_size)

    while run:

        for event in game.event.get():

            if event.type == game.MOUSEBUTTONDOWN:
                mouse_state = game.mouse.get_pressed(3)
                if mouse_state[0]:
                    grid_array = get_mouse_in_array(grid_array, w_grid, h_grid, margin)

            if event.type == game.KEYDOWN:
                if event.key == game.K_SPACE:
                    grid_array = newGen(grid_array, generation)
                    generation += 1

                    print('Current Generation: {}'.format(generation))
                if event.key == game.K_LEFT:
                    if generation > 0:
                        grid_array = generation_dict.get(generation - 1)
                        generation -= 1
                        print('Current Generation: {}'.format(generation))

                if event.key == game.K_f:
                    grid_array = get_mouse_in_array(grid_array, w_grid, h_grid, margin)

                if event.key == game.K_r:
                    grid_array.fill(0)
                    generation = 0

                if event.key == game.K_ESCAPE:
                    run = False

            if event.type == game.QUIT:
                run = False

        screen.fill("black")

        for row in range(size_grid[0]):
            for col in range(size_grid[1]):
                if grid_array[row][col] == 0:
                    game.draw.rect(screen, 'white',
                                   [(margin + w_grid) * col + margin, (margin + h_grid) * row + margin, w_grid, h_grid])
                else:
                    game.draw.rect(screen, 'black',
                                   [(margin + w_grid) * col + margin, (margin + h_grid) * row + margin, w_grid, h_grid])

        game.display.update()


def get_mouse_in_array(array_map, w_grid, h_grid, margin):
    mouse_pos = game.mouse.get_pos()
    if array_map[(mouse_pos[1] // (w_grid + margin))][(mouse_pos[0] // (h_grid + margin))] == 1:
        array_map[(mouse_pos[1] // (w_grid + margin))][(mouse_pos[0] // (h_grid + margin))] = 0
    else:
        array_map[(mouse_pos[1] // (w_grid + margin))][(mouse_pos[0] // (h_grid + margin))] = 1
    return array_map


def newGen(current_map, generation: int):
    generation_dict[generation] = current_map
    current_map_copy = current_map.copy()
    return nextGen(current_map, current_map_copy)


def nextGen(current_map, current_map_copy):
    for row in range(len(current_map[0])):
        for col in range(len(current_map)):
            if current_map[row][col] == 1:
                check = check_neighbor(current_map, row, col)
                if not check[0]:
                    current_map_copy[row][col] = 0
                if check[1] >= 0:
                    for n_row in range(row - 1, row + 2):
                        for n_col in range(col - 1, col + 2):
                            if not (n_row == row and n_col == col):
                                n_check = check_neighbor(current_map, n_row, n_col)
                                if n_check[1] == 3:
                                    current_map_copy[n_row][n_col] = 1
    current_map = current_map_copy
    return current_map


def check_neighbor(current_map_copy, row, col):
    if not (row == 0 or row == SIZE_GRID[0] - 1 or col == 0 or col == SIZE_GRID[1] - 1):
        alive_neighbor = int(np.sum(current_map_copy[row - 1:row + 2, col - 1:col + 2]) - current_map_copy[row, col])

        if 2 <= alive_neighbor < 4:
            return True, alive_neighbor
        elif alive_neighbor > 3 or alive_neighbor < 2:
            return False, alive_neighbor
    else:
        return False, -1


def main():
    grid_array = np.zeros((SIZE_GRID[0], SIZE_GRID[1]), dtype=int)

    run_GameUI(size_grid=SIZE_GRID,
               w_grid=WIDTH_GRID,
               h_grid=HEIGHT_GRID,
               margin=MARGIN,
               run=RUNNING,
               grid_array=grid_array)


if __name__ == '__main__':
    main()
