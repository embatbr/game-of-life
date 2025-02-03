"""This module contains code to describe cellular automatons such as Conway's
Game of Life, as well as variations.
"""


import os
import random
import re

from automata import CellularAutomaton


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


    NUM_MAX_NEIGHBORS = 8


    def __init__(self, class_path, automaton_name, input_name):
        super(LifeLike, self).__init__(class_path, automaton_name)

        self.input_name = input_name
        nums = re.findall(r"\d+", self.automaton_name)
        self.rules = {
            "born": read_rule(nums[0]),
            "survive": read_rule(nums[1])
        }

    @property
    def output_path(self):
        return f"{super(LifeLike, self).output_path}/{self.input_name}"

    def reset(self):
        super(LifeLike, self).reset()

        file = open(f"inputs/{self.class_path}/{self.input_name}")
        lines = file.readlines()

        self.num_rows = int(lines[0][:-1])
        self.num_cols = int(lines[1][:-1])
        self.grid = self.create_grid()

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                char = lines[i + 2][j]
                if char != self.CellStates.DEAD:
                    self.grid[i][j] = char
                    if char == self.CellStates.ALIVE:
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

        if (cell_stage == self.CellStates.DEAD) and (num_neighbors in self.rules["born"]):
            next_cell_stage = self.CellStates.ALIVE
            self.population = self.population + 1
        elif (cell_stage == self.CellStates.ALIVE) and (num_neighbors not in self.rules["survive"]):
            next_cell_stage = self.CellStates.DEAD
            self.population = self.population - 1

        return next_cell_stage


class LifeLikeCancer(LifeLike):
    """Similar to LifeLike, but with more states and different rules.
    """

    class CellStates(object):
        DEAD   = u"\u25A1"
        ALIVE  = u"\u25A3"
        CANCER = u"\u25A9"


    def __init__(self, class_path, automaton_name, input_name, mutation_chance, growth_rate):
        super(LifeLikeCancer, self).__init__(class_path, automaton_name, input_name)

        self.mutation_chance = float(mutation_chance)
        self.growth_rate = int(growth_rate)
        if (self.growth_rate < 1) or (self.growth_rate > 8):
            raise Exception("LifeLikeCancer 'growth_rate' must be in interval [1,8].")

    @property
    def output_path(self):
        return f"{super(LifeLikeCancer, self).output_path}/{self.mutation_chance}-{self.growth_rate}"

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
                num_alive_neighbors = 0
                num_cancer_neighbors = 0
                for ix in [i_minus_1, i, i_plus_1]:
                    for jx in [j_minus_1, j, j_plus_1]:
                        if (ix, jx) != (i, j):
                            if self.grid[ix][jx] == self.CellStates.ALIVE:
                                num_alive_neighbors = num_alive_neighbors + 1
                            elif self.grid[ix][jx] == self.CellStates.CANCER:
                                num_cancer_neighbors = num_cancer_neighbors + 1

                next_cell_stage = self.apply_rules(cell_stage, num_alive_neighbors, num_cancer_neighbors)
                next_grid[i][j] = next_cell_stage

        if (next_grid == self.grid) or (self.population == 0):
            self.finish()

        self.grid = next_grid

    def apply_rules(self, cell_stage, num_alive_neighbors, num_cancer_neighbors):
        next_cell_stage = cell_stage

        if (cell_stage == self.CellStates.DEAD) and (num_cancer_neighbors > 0) and (num_alive_neighbors > 0) and (random.randint(0, self.NUM_MAX_NEIGHBORS) < max(num_cancer_neighbors, self.growth_rate)):
            next_cell_stage = self.CellStates.CANCER
        elif (cell_stage == self.CellStates.DEAD) and (num_alive_neighbors in self.rules["born"]):
            next_cell_stage = self.CellStates.ALIVE
            self.population = self.population + 1
        elif (cell_stage == self.CellStates.ALIVE) and (random.random() < self.mutation_chance):
            next_cell_stage = self.CellStates.CANCER
            self.population = self.population - 1
        elif (cell_stage == self.CellStates.ALIVE) and (num_alive_neighbors not in self.rules["survive"]):
            next_cell_stage = self.CellStates.DEAD
            self.population = self.population - 1
        elif (cell_stage == self.CellStates.CANCER) and (num_alive_neighbors == 0):
            next_cell_stage = self.CellStates.DEAD

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
