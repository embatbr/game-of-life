"""
Singular: automaton
Plural: automata
"""

import os
import time


SLEEP_INTERVAL = 1 # in seconds


class AutomatonStates(object):
    READY    = 0
    RUNNING  = 1
    FINISHED = 2 # no guarantee this one will be reached


class Automaton(object):
    """An automaton is a relatively self-operating machine, or control mechanism
    designed to automatically follow a sequence of operations, or respond to
    predetermined instructions.
    """

    def __init__(self, automaton_name, output_prefix):
        super(Automaton, self).__init__()

        self.automaton_name = automaton_name
        self.output_dirpath = f"{output_prefix}/{self.automaton_name}"

        self.sleep_interval = SLEEP_INTERVAL

    def run(self):
        """Do not change me in subclass. No need for that. Just play along.
        """
        self.write_output()
        self.state = AutomatonStates.RUNNING

        while self.state == AutomatonStates.RUNNING:
            self.process()
            self.iteration = self.iteration + 1

            time.sleep(self.sleep_interval)

            self.write_output()

    def reset(self):
        self.state = AutomatonStates.READY
        self.iteration = 1

    def finish(self):
        self.state = AutomatonStates.FINISHED

    def write_output(self):
        os.makedirs(self.output_dirpath, exist_ok=True)

    def process(self):
        raise NotImplementedError("Method 'process' must be implemented in subclass.")


class CellularAutomaton(Automaton):
    """
    """
    
    def __init__(self, automaton_name, output_prefix):
        super(CellularAutomaton, self).__init__(automaton_name, output_prefix)

    @property
    def generation(self):
        return self.iteration

    def reset(self):
        super(CellularAutomaton, self).reset()
        self.population = 0

    def create_grid(self):
        raise NotImplementedError("Method 'create_grid' must be implemented in subclass.")

    def write_grid(self, file):
        raise NotImplementedError("Method 'write_grid' must be implemented in subclass.")

    def write_output(self):
        super(CellularAutomaton, self).write_output()

        with open(f"{self.output_dirpath}/{self.input_name}", 'w') as file:
            file.write("gen: {}\n".format(self.generation))
            file.write("pop: {}\n".format(self.population))
            self.write_grid(file)
