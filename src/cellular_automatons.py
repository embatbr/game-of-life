"""This module contains code to describe cellular automatons such as Conway's
Game of Life, as well as variations.
"""


import os
import time


PROJECT_ROOT_PATH = os.environ.get("PROJECT_ROOT_PATH")

INPUT_GRID_DIRPATH = f"{PROJECT_ROOT_PATH}/inputs"
OUTPUT_GRID_DIRPATH = f"{PROJECT_ROOT_PATH}/outputs"

SLEEP_INTERVAL = 1 # in seconds


read_rule = lambda x: list(map(int, list(x)))
write_rule = lambda x: ''.join(list(map(str, x)))


class AutomatonStates(object):
    READY    = 0
    RUNNING  = 1
    FINISHED = 2 # no guarantee this one will be reached


class CellStates(object):
    DEAD  = u"\u25A1"
    ALIVE = u"\u25A3"


class LifeLike(object):
    """Base class for a life-like cellular automaton.

    Rules the automaton must follow:

        - 2D array of cells;
        - Two states (dead and alive);
        - Moore neighborhood;
        - New cell state is expressed as a function of the number of adjacent
    cells alive and the cell's own state.
    """

    DEFAULT_GRID_SIZE = 30

    def __init__(self, input_name, newborn, keepalive):
        super(LifeLike, self).__init__()

        self.input_name = input_name
        self.rules = {
            "newborn": newborn,
            "keepalive": keepalive
        }
        self.sleep_interval = SLEEP_INTERVAL

        self.reset()


    @property
    def automaton_name(self):
        newborn = write_rule(self.rules["newborn"])
        keepalive = write_rule(self.rules["keepalive"])
        return f"b{newborn}s{keepalive}"


    def reset(self):
        """Resets the automaton to the initial state.
        """
        self.state = AutomatonStates.READY
        self.generation = 1
        self.population = 0

        file = open(f"{INPUT_GRID_DIRPATH}/{self.input_name}")
        lines = file.readlines()

        self.num_rows = int(lines[0][:-1])
        self.num_cols = int(lines[1][:-1])
        self.grid = self._create_grid()

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                char = lines[i + 2][j]
                if char == CellStates.ALIVE:
                    self.grid[i][j] = CellStates.ALIVE
                    self.population = self.population + 1

        file.close()

    def _create_grid(self):
        return [[CellStates.DEAD for _ in range(self.num_cols)] for _ in range(self.num_rows)]

    def write_grid(self):
        os.makedirs(f"{OUTPUT_GRID_DIRPATH}/{self.automaton_name}", exist_ok=True)

        with open(f"{OUTPUT_GRID_DIRPATH}/{self.automaton_name}/{self.input_name}", 'w') as file:
            file.write("gen: {}\n".format(self.generation))
            file.write("pop: {}\n".format(self.population))
            screen = '\n'.join(''.join(row) for row in self.grid)
            file.write(screen)

    def process(self):
        next_grid = self._create_grid()

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell_stage = self.grid[i][j]

                i_minus_1 = (i - 1) % self.num_rows
                i_plus_1 = (i + 1) % self.num_rows
                j_minus_1 = (j - 1) % self.num_cols
                j_plus_1 = (j + 1) % self.num_cols

                # checking neighbors
                num_neighbors = 0
                for ix in [i_minus_1, i, i_plus_1]:
                    for jx in [j_minus_1, j, j_plus_1]:
                        if ((ix, jx) != (i, j)) and (self.grid[ix][jx] == CellStates.ALIVE):
                                num_neighbors = num_neighbors + 1

                next_cell_stage = self.apply_rules(cell_stage, num_neighbors)
                next_grid[i][j] = next_cell_stage

        if next_grid == self.grid:
            self.state = AutomatonStates.FINISHED

        self.grid = next_grid

    def apply_rules(self, cell_stage, num_neighbors):
        next_cell_stage = cell_stage

        if (cell_stage == CellStates.DEAD) and (num_neighbors in self.rules["newborn"]):
            next_cell_stage = CellStates.ALIVE
            self.population = self.population + 1
        elif (cell_stage == CellStates.ALIVE) and (num_neighbors not in self.rules["keepalive"]):
            next_cell_stage = CellStates.DEAD
            self.population = self.population - 1

        return next_cell_stage

    def run(self):
        self.write_grid()
        self.state = AutomatonStates.RUNNING

        while self.state == AutomatonStates.RUNNING:
            self.process()
            self.generation = self.generation + 1

            time.sleep(self.sleep_interval)

            self.write_grid()


# TODO remove it and parameterize the rules
class LifeLikeB3S23(LifeLike):
    """Conway's Game of Life.
    """

    def __init__(self, input_name):
        super(LifeLikeB3S23, self).__init__(input_name)

    @property
    def automaton_name(self):
        return "b3s23"


if __name__ == "__main__":
    import sys

    newborn = sys.argv[1]
    keepalive = sys.argv[2]
    input_name = sys.argv[3]

    print(f"Running B{newborn}S{keepalive} for input '{input_name}'")

    automaton = LifeLike(input_name, read_rule(newborn), read_rule(keepalive))
    automaton.run()
