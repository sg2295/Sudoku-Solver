# Sudoku Solver
## Introduction
This project is an agent capable of solving Sudoku puzzles of varying difficulties using a backtracking depth-first search algorithm with constraint propagation. The implementation incorporates heuristic functions to make educated decisions when choosing which move to make next.

### Sudoku Puzzles (The Game)



### Sudoku as a Constraint Satisfaction Problem (CSP)

## Approach
Use a **back-tracking search**, following a combination of **depth-first search** (DFS) and **constraint propagation**.
### Heuristics
#### Variable Heuristics
Uses the **minimum-remaining values** (MRV) heuristic, which picks the "most constrained variable" every time it makes a choice. In other words, it chooses the variable that is most likely to result in an invalid state. (Page 216-17)

The algorithm works as follows:
1. Pick the most constrained value
1. Get the resulting state
1. If the state is valid, repeat steps 1-3. Otherwise, exit (no solution exists).

#### Value Heuristics

## Results

## Discussion

## References
[1] Norvig, Peter, Russel, Stuart. *Artificial Intelligence : A Modern Approach 3rd Edition*. Pearson Education, 2016.