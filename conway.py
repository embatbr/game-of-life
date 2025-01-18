"""Original Conway's Game of Life.
"""

import time


INPUT_GRID_DIRPATH = 'inputs'
OUTPUT_GRID_FILEPATH = 'output'

DEAD = u"\u25A1"
ALIVE = u"\u25A3"
ALLOWED_CHARS = set([DEAD, ALIVE])
SLEEP_INTERVAL = 1


class Game(object):
    """Game contains the grid and all the information about the game (generation,
    population and references to the dead and alive positions).
    """

    DEFAULT_GRID_SIZE = 30

    def __init__(self, input_num):
        super(Game, self).__init__()

        self.input_num = input_num

        self.reset()

    def reset(self):
        self.grid = list()
        self.generation = 1
        self.population = 0

        file = open(f"{INPUT_GRID_DIRPATH}/input-{self.input_num}")
        i = 0
        for line in file:
            row = list()

            j = 0
            for char in line:
                if char == '\n':
                    continue

                row.append(char)
                if char == ALIVE:
                    self.population = self.population + 1

                j = j + 1

            self.grid.append(row)

            i = i + 1

    def run(self):
        self.write_grid()

        while True:
            self.apply_rules()
            self.generation = self.generation + 1

            time.sleep(SLEEP_INTERVAL)

            self.write_grid()

    def write_grid(self):
        with open(OUTPUT_GRID_FILEPATH, 'w') as file:
            file.write("gen: {}\n".format(self.generation))
            file.write("pop: {}\n".format(self.population))
            screen = '\n'.join(''.join(row) for row in self.grid)
            file.write(screen)

    def apply_rules(self):
        next_grid = list()

        for i in range(Game.DEFAULT_GRID_SIZE):
            row = list()

            for j in range(Game.DEFAULT_GRID_SIZE):
                cell = self.grid[i][j]

                i_minus_1 = (i - 1) % 30
                i_plus_1 = (i + 1) % 30
                j_minus_1 = (j - 1) % 30
                j_plus_1 = (j + 1) % 30

                num_live_neighbors = 0
                # checking neighbors
                for ix in [i_minus_1, i, i_plus_1]:
                    for jx in [j_minus_1, j, j_plus_1]:
                        if ((ix, jx) != (i, j)) and (self.grid[ix][jx] == ALIVE):
                                num_live_neighbors = num_live_neighbors + 1

                # print(i, j, cell, num_live_neighbors)

                if (cell == ALIVE) and ((num_live_neighbors < 2) or (num_live_neighbors > 3)):
                    cell = DEAD # rules 1, 2 and 3
                    self.population = self.population - 1
                elif (cell == DEAD) and (num_live_neighbors == 3):
                    cell = ALIVE # rule 4
                    self.population = self.population + 1

                row.append(cell)

            next_grid.append(row)

        self.grid = next_grid


if __name__ == "__main__":
    import sys

    input_num = sys.argv[1]
    print(f"Running for input '{input_num}'")
    
    game = Game(input_num)
    game.run()
