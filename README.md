# game-of-life

Conway's Game of Life (and variations in the future)


## Running

A virtual environment is not mandatory, but is a good idea.

1. Create an input in directory *./inputs/<class_path>/*, similar to the ones that already exist:
    - First row is the number of rows for the grid;
    - Second row is the number of columns for the grid;
    - The remaining rows are the "screen", with white (dead) and black (live) squares.
2. Run the shell command `./run.sh (class_path) [kwargs]`:
    - e.g. `./run.sh lifelike.LifeLike automaton_name=b3s23 input_name=001`
3. Let it run until it stops (or not), writing on file *./outputs/<class_path>/<automaton_name>/<input_name>/screen*.


## TODO

- Write class lifelike.LifeLikeCancer:
    - Mutation into cancer cell given a probability in input file;
    - No death (always survive);
    - Use von Neumann neighborhood for tumor growth.
- Make cellular automata that go beyond life-like (several stages, change forks and "stochastic" rules);
- Insert competition between groups in cellular automata.
