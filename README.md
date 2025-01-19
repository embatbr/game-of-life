# game-of-life

Conway's Game of Life (and variations in the future)

## Running

A virtual environment is not mandatory, but is a good idea.

1. Create an input in directory *./inputs/*, similar to the ones that already exist:
    - First row is the number of rows for the grid;
    - Second row is the number of columns for the grid;
    - The remaining rows are the "screen", with white (dead) and black (live) squares.
2. Run the shell command `./run.sh <newborn> <keepalive> <input>`. Example:
    - b3s23: this is Conway's Game of Life and is run as `./run.sh 3 23 <input>`.
3. Let it run until it stops (or not), writing a file in directory *./outputs/*.
