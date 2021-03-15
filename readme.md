# Sudoku Solver
## Introduction
This project is an agent capable of solving Sudoku puzzles of varying difficulties using a backtracking search, by combining **depth-first search** and **constraint propagation**. The implementation incorporates heuristic functions to make educated decisions when choosing which move to make next.

### Sudoku Puzzles (The Game)
Sudoku is a logic-based, number-placement puzzle, where each board consists of a 9x9 grid with a some fixed values. Each position, also called a cell, can hold a value between 1 and 9. A puzzle is completed when each position has been assigned a value, such that each value appears once per row, column, and 3x3 block of the grid.
> Please note that throughout this readme the terms position, cell and variable are used interchangeably.

### Constraint Satisfaction Problems (CSP)
A constraint satisfaction problem (CSP) is a problem that involves a number of variables which can be assigned multiple values, based on some constraints. [1] 

Constraint satisfaction problems can be recognised by the presence of:
- A set of variables, *X = {X<sub>1</sub>, ..., X<sub>n</sub>}*,
- A set of domains, *D = {D<sub>1</sub>, ..., D<sub>n</sub>}* for each variable, and
- A set of constraints *C* which specify the legal combinations of values. [2]

In other terms, each domain *D<sub>i</sub>* contains a set of possible values *{v<sub>1</sub>, ..., v<sub>n</sub>}*, that can be assigned to variable *X<sub>i</sub>*. Additionally, each *v<sub>i</sub>* in a given domain must comply with the constraints defined by *C*.

Constraint satisfaction problems introduce the notion of states and assignments. Russel and Norvig define states as "an assignment of values to some or all of the variables" [2]. Assignments can be **complete** or **partial**. An assignment is called complete when every variable has been assigned a value, while a partial assignment is one where only some variables have been assigned values. An assignment is called **consistent** (or legal) when it adheres to the constraints. If an assignment is both complete and consistent, then it is a **solution** to the problem.

### Sudoku as a Constraint Satisfaction Problem
Sudoku can be represented as a constraint satisfaction problem, where:
- *X = {X<sub>1</sub>, ..., X<sub>n</sub>}* is the set of positions (variables),
- *D<sub>i</sub> = {1, 2, 3, 4, 5, 6, 7, 8, 9}* is the domain describing the values each variable can be assigned (*X<sub>i</sub> ∈ D*), and
- *C = "Each value appears once in each row, column and 3x3 block of the grid "*

## Approach
The Solver makes use of a **backtracking search** algorithm, as explained in Norvig and Russel's *Artificial Intelligence: A Modern Approach*. [2] It uses a depth-first search that is capable of exploring and evaluating assignments, which can now be thought of as nodes. In each iteration, the implementation checks that the assignment is consistent, i.e. that it adheres to the constraints. If the current assignment is not consistent (does not adhere to the constraints), the algorithm backtracks to the last known consistent state and tries a different path. In each stage the algorithm first picks a variable (position) to fill next and then begins testing each of its possible values, exploring and evaluating each assignment. At first, a simple implementation of the algorithm using static variable (and value) ordering was created, and research into dynamic ordering was conducted. To improve the performance of the Solver, in the final implementation, two heuristics were employed to decide variable ordering. **THINK ABOUT VALUE ORDERING**

If the given Sudoku board has a solution, the Solver will find it and return the resulting board configuration as a 2-dimensional `numpy` array. If the board does not have a solution, then the Solver will return a 9x9 `numpy` array filled with `-1`'s, indicating that the given board is unsolvable or is not a valid Sudoku board (i.e. the passed board does not adhere to the constraints).

A more detailed description of the approach can be seen below:
1. The Solver is invoked by calling the `sudoku_solver` function in the driver code segment, and passing in the initial board configuration. The Solver then checks if the given board adheres to the constraints, returning a 9x9 matrix of `-1`'s if it does not. It then evaluates whether the given board is a complete assignment (i.e. if it is already solved), to cover edge cases. 
1. After the initial checks, the possible moves for each position of the board are initialized through `init_constraints`. This function iterates through each variable, defining its domain based on the problem's constraints. This process is computationally expensive and as such is only called once per Sudoku board. To update the possible moves for an assignment later on in the algorithm, the possible moves of the previous state are copied over and updated. This approach proved particularly effective in optimizing the performance of the algorithm.
1. Once the possible values for each variable have been initialized, the `depth_first_search` function is called. This function implements the algorithm explained previously, combining a depth-first search and constraint propagation. It utilizes two heuristics for variable ordering, namely the *minimum-remaining-values* and *degree* heuristics. Both of these heuristics are explained further in the *Heuristics* sub-section below. After each call, the function decides which position to fill next and begins evaluating the possible outcomes. If any assignment is not consistent, the algorithm backtracks to the last known consistent assignment and tries a different path. To explore a given state further, the function makes a recursive call, repeating this process until an inconsistent state or solution is encountered. To create a new board state, the function makes use of `gen_next_state`.
1. The `gen_next_state` function efficiently creates a copy of the current `SudokuState` object, assigns a value to the variable in question, and uses the `update_constraints` function to propagate the constraints for the resulting board (i.e. updates all possible moves for the empty positions). At this point, the function does an additional check to detect any singleton positions in the board, through `get_singletons`. This function finds any empty positions that have only one possible value, following the recent assignment, and returns them. These positions are then assigned their unique possible value. This process is repeated for each variable assignment. The resulting `SudokuState` object is returned to the `deep_first_function` and is evaluated.

### Heuristics
The Solver utilizes of two heuristics to make an informed decision regarding which empty position to pick next. These are the **minimum-remaining-values** (MRV) and **degree** heuristics and are used for variable ordering. Their respective functions are invoked by the `pick_next` function in the driver code segment. By adding these heuristics and removing the previous static variable ordering, the runtime of the solution improved greatly.

#### Minimum-remaining-values (MRV)  Heuristic
The minimum-remaining-values heuristic, also called the "most constrained variable" heuristic, picks the position (variable) with the fewest possible values. [2] It picks the variable that has the highest likelihood of resulting in failure soon, reducing the number of computations otherwise spent searching other variables first. By extent, if a variable has no possible values left then it would be selected and result in failure straight away. It is implemented in the `get_min_value_positions` function. Note that multiple variables can have the same number of possible values, and as such the MRV heuristic may return a list of variables. In this case, the *degree* heuristic is used as a tie-breaker. 

#### Degree Heuristic
The degree heuristic selects the variable with the most constraints on other unassigned variables, i.e. the one that affects the greatest number of empty positions. [2] It is used when the MRV returns multiple variables, to decide which position should be picked - instead of statically ordering the variables. The degree heuristic is split among two functions; the `pick_next` and `get_degree` functions. The latter calculates the "degree" of each position (the number of other empty positions it affects), while the `pick_next` function finds the variable with the maximum degree and returns it. **By using this heuristic, the solution requires less steps as it is not as likely it would need to backtrack CHECK** <--- FIX

## Results and Discussion
### Results
Prior to including heuristics in the solution, the solver would use static variable ordering which does not typically result in an efficient search. [2] By including variable ordering heuristics, the overall runtime of the solution improved drastically. In particular, the greatest change was noticed when the minimum-remaining-values heuristic was added to the implementation. However, by pairing MRV with the degree heuristic, the runtime was significantly improved once more, resulting in a total runtime of 5.1 - 6.2 second for all tests.

### Value Ordering MAYBE INCLUDE ? COULD BE MOVED TO FUTURE WORK ? **TODO**
Least-constrained value was added in a previous iteration of the solution, but it was found that the heuristic resulted in slightly increased runtimes, as a notable portion of the time was spent trying to order the values. This was mainly due restrictions of the implementation, requiring two parallel lists to be sorted for every decision. Choice of sorting algorithms did not improve this and after implementing insertion sort, which is ideal for small data sets, it was decided that this heuristic should be removed.

### Code Optimization TODO
**In order for the agent to be able to solve hard Sudoku puzzles in a small timeframe, the implementation had to be optimized. In this capacity, the choice of data structures and algorithms used was a key area that was explored, following a the completetion of the first iteration of the agent.** <------ **TODODDOOD**

Multi-dimensional `numpy` arrays were chosen as the main data structure to store information in the solution. By using a universal data type throughout the solution, the computational costs associated with conversions from one data type to another are avoided. `numpy` arrays were chosen over other alternatives, like python's `list` objects, as they provide in-built functions to iterate and manipulate their contents efficiently, like `ndenumarate`, `ndindex` and `full`. Additionally, the library provides a way of importing Sudoku puzzles from external files directly into a `numpy` array without the need of complex, expensive operations, aiding both code clarity and efficiency.

Other data structures like `dictionaries` and `lists` are also used in certain parts of the solution, namely in the heuristic functions. These however, do not alter the representation of the Sudoku board (`SudokuState`) and are solely used in the functions to improve code complexity at the cost of space complexity.

Through time analysis of the solution, via a code profiler, the `deepcopy` of the `copy` library was proven to take up over 78% of the solution's runtime. To overcome the overheads associated with `deepcopy`, the implementation includes the `copy_state` function which is capable of creating a copy of a `SudokuState` object more efficiently. It achieves this by making use of `numpy`'s inbuilt `ndarray.copy` function. Additionally, by utilizing the **SINGLETONS** <----- TODO DODODODO

### Future Work TODO
An *Inference* function, implementing arc-consistency, could be incorporated in the existing backtracking search. This could potentially improve the overall performance of the solution, since it would be able to detect assignments which lead to failure early on. In particular the *naked triples* heuristic, as explained by Russel and Norvig [2] should be researched further.**TODO**

Multi-threading was beyond the scope of this project and as such was not included in the current implementation. However, it poses an area for further research. By successfully incorporating multi-threading in the solution, the overall runtime of the application would improve.

Apart from a constraint satisfaction problem, Sudoku can also be represented as an exact cover problem. Exact cover problems are decision problems which can be represented by a set and a collection of its subsets. Knuth's *Algorithm X* is capable of solving exact cover problems and if implemented correctly using *Dancing links* is a very efficient approach. [3] As further work, this approach should be explored further, implemented and compared with the current solution.

## References
[1] Rossi, F., 2006. *Handbook of constraint programming*. Amsterdam: Elsevier.

[2] Norvig, P., Russel, S., 2016. *Artificial Intelligence: A Modern Approach*. Third Edition. Harlow: Pearson Education.

[3] Knuth, D. E., 2000. *Dancing links* [Online]. Stanford: University of Stanford. Available from: https://arxiv.org/pdf/cs/0011047.pdf [Accessed 14 June 2021].
