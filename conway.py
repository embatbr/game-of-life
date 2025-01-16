"""Original Conway's Game of Life.
"""

import random
import time


GRID_FILEPATH = 'grid'

WHITE_SQUARE = u"\u25A1"
BLACK_SQUARE = u"\u25A3"


def generate_grid(size, seed=[]):
    """Generates a squared grid.
    """
    grid = list()

    for i in range(size):
        row = list()
        for j in range(size):
            row.append(WHITE_SQUARE)
        grid.append(row)

    return grid


def write_grid(grid, generation, population):
    with open(GRID_FILEPATH, 'w') as file:
        screen = '\n'.join(''.join(row) for row in grid)
        file.write("{}\n".format(generation))
        file.write("{}\n".format(population))
        file.write(screen)


if __name__ == "__main__":
    size = 50
    grid = generate_grid(size)
    generation = 1
    write_grid(grid, generation, 0)

    while True:
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        grid[i][j] = BLACK_SQUARE
        write_grid(grid, generation, 0)

        generation += 1
        time.sleep(1)