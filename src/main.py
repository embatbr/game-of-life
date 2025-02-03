"""Entrance point for running the automata. This module, when directly executed, receives the class
to execute, as well as its arguments. 
"""


import importlib
import re
import sys


CLASS_PATH_PATTERN = r"^[a-zA-z]+\.[A-z]+[a-zA-z]*$" # TODO add packages and submodules
CLASS_PATH_REGEX = re.compile(CLASS_PATH_PATTERN)


if __name__ == "__main__":
    class_path = sys.argv[1]
    class_args = sys.argv[2:]

    if not CLASS_PATH_REGEX.match(class_path):
        raise Exception("Class path must be like 'module.Class'.")

    splitted = re.split(r"\.", class_path)
    module_name = splitted[0]
    class_name = splitted[1]

    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)
    
    kwargs = {arg.split('=')[0]:arg.split('=')[1] for arg in class_args}

    automaton = class_obj(class_path, **kwargs)
    print(f"Running '{class_path}' with arguments \"{kwargs}\".")
    print(f"See outputs in '{automaton.output_path}'")
    automaton.run()
