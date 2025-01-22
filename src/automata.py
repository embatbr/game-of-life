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
    
    def __init__(self, automaton_name, output_dirpath):
        super(Automaton, self).__init__()

        self.automaton_name = automaton_name
        self.output_dirpath = f"{output_dirpath}/{self.automaton_name}"

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

    def write_output(self):
        os.makedirs(self.output_dirpath, exist_ok=True)

    def process(self):
        raise NotImplementedError("Method 'process' must be implemented in subclass.")
