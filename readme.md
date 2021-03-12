## Sudoku Solver
Use a **back-tracking search**, following a combination of **depth-first search** (DFS) and **constraint propagation**.

Uses the **minimum-remaining values** (MRV) heuristic, which picks the "most constrained variable" every time it makes a choice. In other words, it chooses the variable that is most likely to result in an invalid state. (Page 216-17)
  
The algorithm works as follows:
1. Pick the most constrained value
1. Get the resulting state
1. If the state is valid, repeat steps 1-3. Otherwise, exit (no solution exists).

