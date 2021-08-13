import pygame as game
import numpy as np

# import pygame_gui as gui

RUNNING = True
SIZE_GRID = 200, 200
WIDTH_GRID, HEIGHT_GRID = 7, 7
MARGIN = 1
TIMER = 25  # recommended min time => 25ms


def run_GameUI(size_grid, w_grid, h_grid, margin, run, map_array):
    window_size = size_grid[0] * (w_grid + margin), size_grid[1] * (h_grid + margin)
    game.init()
    # width, height = window_size
    sim_run = False
    run_first = True

    generation_dict = {}
    generation = 0

    game.display.set_caption("Game of Life")
    screen = game.display.set_mode(window_size)

    while run:

        for event in game.event.get():

            if event.type == game.MOUSEBUTTONDOWN:
                mouse_state = game.mouse.get_pressed(3)
                if mouse_state[0]:
                    map_array, killed_cells = get_mouse_in_array(map_array, w_grid, h_grid, margin)
                    if len(killed_cells) > 0:
                        update_map(map_array, generation_dict, generation, screen, killed_cells, w_grid, h_grid, margin)

            if event.type == game.KEYDOWN:
                if event.key == game.K_SPACE:
                    map_array = newGen(map_array, generation, generation_dict)
                    generation += 1
                    print_generations(generation)

                if event.key == game.K_LEFT:
                    if generation > 0:
                        draw_new_map(screen, size_grid, w_grid, h_grid, margin)
                        map_array = generation_dict.get(generation - 1)
                        generation -= 1
                        print_generations(generation)

                if event.key == game.K_s:
                    sim_run = not sim_run
                    game.time.set_timer(game.NUMEVENTS - 5, TIMER)

                if event.key == game.K_r:
                    map_array.fill(0)
                    draw_new_map(screen, size_grid, w_grid, h_grid, margin)
                    generation_dict.clear()
                    generation = 0

                if event.key == game.K_t:
                    map_array, generation = \
                        time_machine(map_array, generation, int(input("Time Machine : Type a generation\n")),
                                     generation_dict)
                    print_generations(generation)

                if event.key == game.K_ESCAPE:
                    run = False

            if event.type == game.QUIT:
                run = False

            if sim_run:
                if event.type == game.NUMEVENTS - 5:
                    map_array, generation = run_simulation(map_array, generation, generation_dict)
                    print_generations(generation)
                    game.time.set_timer(game.NUMEVENTS - 5, TIMER)

        if run_first:
            draw_new_map(screen, size_grid, w_grid, h_grid, margin)
            run_first = False

        update_map(map_array, generation_dict, generation, screen, [], w_grid, h_grid, margin)

        game.display.update()


def update_map(map_array, generation_dict, generation, screen, killed_cells, w_grid, h_grid, margin):
    living_cells = find_all_cells(map_array)
    for cell in living_cells:
        game.draw.rect(screen, 'black',
                       [(margin + w_grid) * cell[1] + margin, (margin + h_grid) * cell[0] + margin, w_grid, h_grid])
    if len(killed_cells) > 0:
        game.draw.rect(screen, 'white',
                       [(margin + w_grid) * killed_cells[1] + margin, (margin + h_grid) * killed_cells[0] + margin,
                        w_grid, h_grid])

    if generation > 0:
        if len(generation_dict) > 0:
            dead_cells = find_all_cells(
                np.bitwise_and(np.bitwise_and(np.bitwise_or(generation_dict[generation - 1], map_array),
                                              np.bitwise_or(np.bitwise_not(generation_dict[generation - 1]),
                                                            np.bitwise_not(map_array))),
                               np.bitwise_or(generation_dict[generation - 1], np.bitwise_not(map_array))))

            for cell in dead_cells:
                game.draw.rect(screen, 'white',
                               [(margin + w_grid) * cell[1] + margin, (margin + h_grid) * cell[0] + margin, w_grid, h_grid])


def find_all_cells(map_array):
    living_cells = []
    row, col = np.where(map_array == 1)
    if (len(row) and len(col)) > 0:
        for i in range(len(row)):
            living_cells.append([row[i], col[i]])
    return living_cells


def draw_new_map(screen, size_grid, w_grid, h_grid, margin):
    for row in range(size_grid[0]):
        for col in range(size_grid[1]):
            game.draw.rect(screen, 'white',
                           [(margin + w_grid) * col + margin, (margin + h_grid) * row + margin, w_grid, h_grid])


def print_generations(generation):
    print("Current Generations: {}".format(generation))


def run_simulation(map_array, generation, generation_dict):
    map_array = newGen(map_array, generation, generation_dict)
    generation += 1
    return map_array, generation


def time_machine(map_array, generation_current, generation_limit, generation_dict):
    generation = generation_current
    for i in range(generation_limit):
        map_array = newGen(map_array, generation, generation_dict)
        generation += 1
    return map_array, generation


def get_mouse_in_array(map_array, w_grid, h_grid, margin):
    mouse_pos = game.mouse.get_pos()
    if map_array[(mouse_pos[1] // (w_grid + margin))][(mouse_pos[0] // (h_grid + margin))] == 1:
        map_array[(mouse_pos[1] // (w_grid + margin))][(mouse_pos[0] // (h_grid + margin))] = 0
        return map_array, [(mouse_pos[1] // (w_grid + margin)), (mouse_pos[0] // (h_grid + margin))]
    else:
        map_array[(mouse_pos[1] // (w_grid + margin))][(mouse_pos[0] // (h_grid + margin))] = 1
        return map_array, []


def newGen(current_map, generation: int, generation_dict):
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
    map_array = np.zeros((SIZE_GRID[0], SIZE_GRID[1]), dtype=int)

    run_GameUI(size_grid=SIZE_GRID,
               w_grid=WIDTH_GRID,
               h_grid=HEIGHT_GRID,
               margin=MARGIN,
               run=RUNNING,
               map_array=map_array)


if __name__ == '__main__':
    main()
