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

    def __init__(self, class_path, automaton_name):
        super(Automaton, self).__init__()

        self.class_path = class_path
        self.automaton_name = automaton_name

        self.sleep_interval = SLEEP_INTERVAL

    @property
    def output_path(self):
        return f"outputs/{self.class_path}/{self.automaton_name}"

    def run(self):
        """Do not change me in subclass. No need for that. Just play along.
        """
        self.reset()

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
        os.makedirs(self.output_path, exist_ok=True)

    def process(self):
        raise NotImplementedError("Method 'process' must be implemented in subclass.")


class CellularAutomaton(Automaton):
    """
    """
    
    def __init__(self, class_path, automaton_name):
        super(CellularAutomaton, self).__init__(class_path, automaton_name)

    @property
    def generation(self):
        return self.iteration

    @property
    def screen_output_path(self):
        return f"{self.output_path}/screen"

    @property
    def history_output_path(self):
        return f"{self.output_path}/history"

    def reset(self):
        super(CellularAutomaton, self).reset()
        self.population = 0

        if os.path.exists(self.history_output_path) and os.path.isfile(self.history_output_path):
            os.remove(self.history_output_path)

    def create_grid(self):
        raise NotImplementedError("Method 'create_grid' must be implemented in subclass.")

    def write_grid(self, file):
        raise NotImplementedError("Method 'write_grid' must be implemented in subclass.")

    def write_output(self):
        super(CellularAutomaton, self).write_output()

        with open(self.screen_output_path, 'w') as file:
            file.write("gen: {}\n".format(self.generation))
            file.write("pop: {}\n".format(self.population))
            self.write_grid(file)

        with open(self.history_output_path, 'a') as file:
            file.write("gen: {}\n".format(self.generation))
            file.write("pop: {}\n".format(self.population))
            self.write_grid(file)
            file.write('\n')
