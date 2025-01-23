"""This module contains code to describe cellular automatons such as Conway's
Game of Life, as well as variations.
"""


import os
import re

from automata import CellularAutomaton


PROJECT_ROOT_PATH = os.environ.get("PROJECT_ROOT_PATH")

INPUT_PREFIX = f"{PROJECT_ROOT_PATH}/inputs/lifelike"
OUTPUT_PREFIX = f"{PROJECT_ROOT_PATH}/outputs/lifelike"

AUTOMATON_NAME_PATTERN = r"^(b|B)[0-9]+(s|S)[0-9]+$"
AUTOMATON_NAME_REGEX = re.compile(AUTOMATON_NAME_PATTERN)


read_rule = lambda x: list(map(int, list(x)))


class LifeLike(CellularAutomaton):
    """Base class for a life-like cellular automaton.

    Rules the automaton must follow:

        - 2D array of cells;
        - Two states (dead and alive);
        - Moore neighborhood;
        - New cell state is expressed as a function of the number of adjacent
    cells alive and the cell's own state.
    """

    class CellStates(object):
        DEAD  = u"\u25A1"
        ALIVE = u"\u25A3"


    def __init__(self, automaton_name, input_name):
        super(LifeLike, self).__init__(automaton_name, OUTPUT_PREFIX)

        self.input_name = input_name
        nums = re.findall(r"\d+", self.automaton_name)
        self.rules = {
            "newborn": read_rule(nums[0]),
            "keepalive": read_rule(nums[1])
        }

        self.reset()

    def reset(self):
        super(LifeLike, self).reset()

        file = open(f"{INPUT_PREFIX}/{self.input_name}")
        lines = file.readlines()

        self.num_rows = int(lines[0][:-1])
        self.num_cols = int(lines[1][:-1])
        self.grid = self.create_grid()

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                char = lines[i + 2][j]
                if char == self.CellStates.ALIVE:
                    self.grid[i][j] = self.CellStates.ALIVE
                    self.population = self.population + 1

        file.close()

    def create_grid(self):
        """Creates a 2D grid.
        """
        return [[self.CellStates.DEAD for _ in range(self.num_cols)] for _ in range(self.num_rows)]

    def write_grid(self, file):
        screen = '\n'.join(''.join(row) for row in self.grid)
        file.write(screen)

    def process(self):
        next_grid = self.create_grid()

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
                        if ((ix, jx) != (i, j)) and (self.grid[ix][jx] == self.CellStates.ALIVE):
                                num_neighbors = num_neighbors + 1

                next_cell_stage = self.apply_rules(cell_stage, num_neighbors)
                next_grid[i][j] = next_cell_stage

        if next_grid == self.grid:
            self.finish()

        self.grid = next_grid

    def apply_rules(self, cell_stage, num_neighbors):
        next_cell_stage = cell_stage

        if (cell_stage == self.CellStates.DEAD) and (num_neighbors in self.rules["newborn"]):
            next_cell_stage = self.CellStates.ALIVE
            self.population = self.population + 1
        elif (cell_stage == self.CellStates.ALIVE) and (num_neighbors not in self.rules["keepalive"]):
            next_cell_stage = self.CellStates.DEAD
            self.population = self.population - 1

        return next_cell_stage


if __name__ == "__main__":
    import sys

    automaton_name = sys.argv[1]
    input_name = sys.argv[2]

    if AUTOMATON_NAME_REGEX.match(automaton_name):
        print(f"Running {automaton_name} for input '{input_name}'")

        automaton = LifeLike(automaton_name, input_name)
        automaton.run()
    else:
        print("Wrong game type.")
