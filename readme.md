# Sudoku Solver
## Introduction
This project is an agent capable of solving Sudoku puzzles of varying difficulties using a backtracking search, by combining depth-first search and constraint propagation. The implementation incorporates heuristic functions to make educated decisions when choosing which move to make next.

### Sudoku Puzzles (The Game)
Sudoku is a logic-based, number-placement puzzle. Each board consists of a 9x9 grid with a some fixed values. Each position, also called a cell, can hold a value between 1 and 9. A puzzle is completed when each position has been assigned a value, such that each value appears once per row, column, and 3x3 block of the grid.

### Constraint Satisfaction Problems (CSP)
A constraint satisfaction problem (CSP) is a problem that involves a number of variables which can be assigned multiple values, based on some constraints. [1] 

Alternatively, constraint satisfaction problems can be recognised by the presence of:
- A set of variables, *X = {X<sub>1</sub>, ..., X<sub>n</sub>}*,
- A set of domains, *D = {D<sub>1</sub>, ..., D<sub>n</sub>}* for each variable, and
- A set of constraints *C* which specify the legal combinations of values. [2]

Where domain *D<sub>i</sub>* contains a set of possible values *{v<sub>1</sub>, ..., v<sub>n</sub>}*, that can be assigned to variable *X<sub>i</sub>*. Additionally, each *v<sub>i</sub>* in a given domain must comply with the constraints defined by *C*.

Constraint satisfaction problems make use of 

### Sudoku as a CSP

## Approach
Use a **back-tracking search**, following a combination of **depth-first search** (DFS) and **constraint propagation**.
### Heuristics
#### Variable Heuristics
Uses the **minimum-remaining values** (MRV) heuristic, which picks the "most constrained variable" every time it makes a choice. In other words, it chooses the variable that is most likely to result in an invalid state. (Page 216-17)

The algorithm works as follows:
1. Pick the most constrained value
1. Get the resulting state
1. If the state is valid, repeat steps 1-3. Otherwise, exit (no solution exists).

#### Value Heuristics TODO

## Results

## Discussion

## References
[1] Rossi, Francesca. *Handbook of constraint programming*. Elsevier, 2006.

[2] Norvig, Peter, Russel, Stuart. *Artificial Intelligence: A Modern Approach 3rd Edition*. Pearson Education, 2016.