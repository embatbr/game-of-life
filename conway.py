"""Original Conway's Game of Life.
"""

import time


INPUT_GRID_DIRPATH = 'inputs'
OUTPUT_GRID_DIRPATH = 'outputs'

COMMENT_MARK = "#"

DEAD = u"\u25A1"
ALIVE = u"\u25A3"
SLEEP_INTERVAL = 1


class Game(object):
    """Game contains the grid and all the information about the game (generation,
    population and references to the dead and alive positions).
    """

    DEFAULT_GRID_SIZE = 30

    def __init__(self, game_name, size=DEFAULT_GRID_SIZE, sleep_interval=SLEEP_INTERVAL):
        super(Game, self).__init__()

        self.game_name = game_name
        self.size = size
        self.sleep_interval = sleep_interval

        self.keep_running = True

        self.reset()

    def reset(self):
        self.grid = [[DEAD for _ in range(self.size)] for _ in range(self.size)]
        self.generation = 1
        self.population = 0

        file = open(f"{INPUT_GRID_DIRPATH}/{self.game_name}")

        i = 0
        for line in file:
            if line.strip().startswith(COMMENT_MARK):
                continue

            j = 0
            for char in line:
                if char == ALIVE:
                    self.grid[i][j] = ALIVE
                    self.population = self.population + 1

                j = j + 1
            i = i + 1

    def run(self):
        self.write_grid()

        while self.keep_running:
            self.apply_rules()
            self.generation = self.generation + 1

            time.sleep(self.sleep_interval)

            self.write_grid()

    def write_grid(self):
        with open(f"{OUTPUT_GRID_DIRPATH}/{self.game_name}", 'w') as file:
            file.write("gen: {}\n".format(self.generation))
            file.write("pop: {}\n".format(self.population))
            screen = '\n'.join(''.join(row) for row in self.grid)
            file.write(screen)

    def apply_rules(self):
        grid_next_stage = [[DEAD for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                cell = self.grid[i][j]
                cell_next_stage = cell

                i_minus_1 = (i - 1) % self.size
                i_plus_1 = (i + 1) % self.size
                j_minus_1 = (j - 1) % self.size
                j_plus_1 = (j + 1) % self.size

                # checking neighbors
                num_neighbors = 0
                for ix in [i_minus_1, i, i_plus_1]:
                    for jx in [j_minus_1, j, j_plus_1]:
                        if ((ix, jx) != (i, j)) and (self.grid[ix][jx] == ALIVE):
                                num_neighbors = num_neighbors + 1

                if (cell == ALIVE) and ((num_neighbors < 2) or (num_neighbors > 3)): # rules 1, 2 and 3
                    cell_next_stage = DEAD
                    self.population = self.population - 1
                elif (cell == DEAD) and (num_neighbors == 3): # rule 4
                    cell_next_stage = ALIVE
                    self.population = self.population + 1

                grid_next_stage[i][j] = cell_next_stage

        if grid_next_stage == self.grid:
            self.keep_running = False

        self.grid = grid_next_stage


if __name__ == "__main__":
    import sys

    game_name = sys.argv[1]
    print(f"Running for input '{game_name}'")
    
    game = Game(game_name)
    game.run()
