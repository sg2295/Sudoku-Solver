# Sudoku Solver
## Introduction
This project is an agent capable of solving Sudoku puzzles of varying difficulties using a backtracking search, by combining **depth-first search** and **constraint propagation**. The implementation incorporates heuristic functions to make educated decisions when choosing which move to make next.

### Sudoku Puzzles (The Game)
Sudoku is a logic-based, number-placement puzzle. Each board consists of a 9x9 grid with a some fixed values. Each position, also called a cell, can hold a value between 1 and 9. A puzzle is completed when each position has been assigned a value, such that each value appears once per row, column, and 3x3 block of the grid.

### Constraint Satisfaction Problems (CSP)
A constraint satisfaction problem (CSP) is a problem that involves a number of variables which can be assigned multiple values, based on some constraints. [1] 

Constraint satisfaction problems can be recognised by the presence of:
- A set of variables, *X = {X<sub>1</sub>, ..., X<sub>n</sub>}*,
- A set of domains, *D = {D<sub>1</sub>, ..., D<sub>n</sub>}* for each variable, and
- A set of constraints *C* which specify the legal combinations of values. [2]

Where domain *D<sub>i</sub>* contains a set of possible values *{v<sub>1</sub>, ..., v<sub>n</sub>}*, that can be assigned to variable *X<sub>i</sub>*. Additionally, each *v<sub>i</sub>* in a given domain must comply with the constraints defined by *C*.

Constraint satisfaction problems introduce the notion of states and assignments. Russel and Norvig define states as "an assignment of values to some or all of the variables" [2]. Assignments can be **complete** or **partial**. An assignment is called complete when every variable has been assigned a value, while a partial assignment is one that only some variables have been assigned values. An assignment is called **consistent** (or legal) when it adheres to the constraints. If an assignment is both complete and consistent, then it is a **solution** to the problem.

### Sudoku as a Constraint Satisfaction Problem
Sudoku can be represented as a constraint satisfaction problem, where:
- *X = {X<sub>1</sub>, ..., X<sub>n</sub>}* is the set of variables,
- *D<sub>i</sub> = {1, 2, 3, 4, 5, 6, 7, 8, 9}* is the domain describing the values each variable can be assigned (*X<sub>i</sub> ∈ D*), and
- *C = "Each value appears once in each row, column and 3x3 block of the grid "*

## Approach TODO
Employ a **back-tracking search**, using a combination of **depth-first search** (DFS) and **constraint propagation**.



### Heuristics TODO
Two heuristics are used to make an informed decision regarding which empty position to fill next. These are the **minimum-remaining-values** (MRV) and **degree** heuristics and are used for variable ordering.
#### Minimum-remaining-values (MRV)  TODO
The minimum-remaining-values heuristic, also called the "most constrained variable" heuristic, picks the position (variable) with the fewest possible values. [2] It picks a variable that has the highest likelihood of resulting in failure soon, reducing the number of computations otherwise spent searching other variables first. By extent, if a variable has no possible values left then it would be selected and result in failure straight away.

#### Degree  TODO
Since more than one variable (position) can have the same number of possible values, the MRV heuristic can return more than one variable. The degree heuristic is then used as a tie-breaker. The degree heuristic selects the variable with the most constraints on other unassigned variables, i.e. the position that affects the greatest number of empty positions. [2] To decide which position returned by the MRV heuristic should be picked, the degree heuristic function calculates the degree of each position (the number of other empty positions it affects) and returns the maximum.

#### OLD VERSION (REMOVE)
Uses the **minimum-remaining-values** (MRV) heuristic, which picks the "most constrained variable" every time it makes a choice. In other words, it chooses the variable that is most likely to result in an invalid state. (Page 216-17)

The algorithm works as follows:
1. Pick the most constrained value
1. Get the resulting state
1. If the state is valid, repeat steps 1-3. Otherwise, exit (no solution exists).



#### Value Heuristics TODO !!! (PLACEHOLDER, PENDING) TO BE REMOVED
- ADD LEAST-CONSTRAINED VALUE to be removed


## Results TODO
Prior to including heuristics in the solution, the solver would use static variable ordering which does not typically result in an efficient search. [2] By including variable ordering heuristics, the overall runtime of the solution improved drastically. In particular, the greatest change was noticed when the minimum-remaining-values heuristic was added to the solution. However, by pairing MRV with the degree heuristic, the runtime was significantly improved once more, resulting in 8.4 - 9.3 second runtimes for all puzzles.


## Discussion
### Code Optimization
In order for the agent to be able to solve hard Sudoku puzzles in a small timeframe, the implementation had to be optimized. In this capacity, the choice of data structures and algorithms used was 

Multi-dimensional `numpy` arrays were chosen as the main data structure to store information in the solution. By using a universal data type throughout the solution, the computational costs associated with conversions from one data type to another are avoided. `numpy` arrays were chosen over other alternatives, like python's `list` objects, as they provide in-built functions to iterate and manipulate their contents efficiently, like `ndenumarate`, `ndindex` and `full`. Additionally, the library provides a way of importing Sudoku puzzles from external files directly into a `numpy` array without the need of complex, expensive operations, aiding both code clarity and efficiency.

Other data structures like `dictionaries` and `lists` are also used in certain parts of the solution, namely in the heuristic functions. These however, do not alter the representation of the Sudoku board (`SudokuState`) and are solely used in the functions to improve code complexity at the cost of space complexity.

Through time analysis of the solution, via a code profiler, the `deepcopy` of the `copy` library was proven to take up over 78% of the solution's runtime. To overcome the overheads associated with `deepcopy`, the implementation includes the `copy_state` function which is capable of creating a copy of a `SudokuState` object more efficiently. It achieves this by making use of `numpy`'s inbuilt `ndarray.copy` function.

### Future Work
Multi-threading was beyond the scope of this project and as such was not included in the current implementation. However, it poses an area for further research. By successfully incorporating multi-threading in the solution, the overall runtime of the application would improve.

Apart from a constraint satisfaction problem, Sudoku can also be represented as an exact cover problem. Exact cover problems are decision problems which can be represented by a set and a collection of its subsets. Knuth's *Algorithm X* is capable of solving exact cover problems and if implemented correctly using *Dancing links* is a very efficient approach. [3] As further work, this approach should be explored further, implemented and compared with the current solution.

## References
[1] Rossi, F., 2006. *Handbook of constraint programming*. Amsterdam: Elsevier.

[2] Norvig, P., Russel, S., 2016. *Artificial Intelligence: A Modern Approach*. Third Edition. Harlow: Pearson Education.

[3] Knuth, D. E., 2000. *Dancing links* [Online]. Stanford: University of Stanford. Available from: https://arxiv.org/pdf/cs/0011047.pdf [Accessed 14 June 2021].
