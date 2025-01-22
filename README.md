# game-of-life

Conway's Game of Life (and variations in the future)


## Running

A virtual environment is not mandatory, but is a good idea.

1. Create an input in directory *./inputs/lifelike/*, similar to the ones that already exist:
    - First row is the number of rows for the grid;
    - Second row is the number of columns for the grid;
    - The remaining rows are the "screen", with white (dead) and black (live) squares.
2. Run the shell command `./run.sh <module> <automaton_name> <input_name>`:
    - `<module>`: e.g., `lifelike` for a life-like type of automaton;
    - `<automaton_name>` pattern is r"^(b|B)[0-9]+(s|S)[0-9]+$";
    - For example, "b3s23" is Conway's Game of Life and runs as `./run.sh b3s23 <input_name>`.
3. Let it run until it stops (or not), writing a file in directory *./outputs/<module>/<automaton_name>/<input_name>*.


## TODO

- Create a subclass `CellularAutomaton` of class `Automaton`;
- Make cellular automata that go beyond life-like (several stages, change forks and "stochastic" rules);
- Insert competition between groups in cellular automata.
