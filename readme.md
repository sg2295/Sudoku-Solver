# Sudoku Solver
## Introduction
This project is an agent capable of solving Sudoku puzzles of varying difficulties using a backtracking search, by combining **depth-first search** and **constraint propagation**. The implementation incorporates heuristic functions to make informed decisions when choosing which move to make next.

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
- *D<sub>i</sub> = {1, 2, 3, 4, 5, 6, 7, 8, 9}* is the domain describing the values each variable can be assigned (*X<sub>i</sub> ??? D*), and
- *C = "Each value appears once in each row, column and 3x3 block of the grid"* is the set of constraints.

## Approach
The Solver makes use of a **backtracking search** algorithm, as explained in Norvig and Russel's *Artificial Intelligence: A Modern Approach*. [2] It uses a **depth-first search** that is capable of exploring and evaluating assignments, which can now be thought of as nodes. In each iteration, the Solver checks that the assignment is consistent, i.e. that it adheres to the constraints. If the current assignment is not consistent (does not adhere to the constraints), the algorithm backtracks to the last known consistent state and tries a different path. In each stage, the algorithm picks a variable (position) to fill next and then begins testing each of its possible values, exploring and evaluating each assignment. The first implementation of the Solver used static variable (and value) ordering. To improve the performance of the Solver, the final implementation included two heuristics to deal with variable ordering, which are explained further in the *Heuristics* sub-section.

If the Solver is given a Sudoku board that has a solution, it will find it and return the resulting board configuration as a 2-dimensional `numpy` array. If the given board does not have a solution, then the Solver will return a 9x9 `numpy` array filled with `-1`'s, indicating that the given board is unsolvable or that it is not a valid Sudoku board (i.e. the passed board does not adhere to the constraints).

A more detailed description of the approach can be seen below:
1. The Solver is invoked by calling the `sudoku_solver` function in the driver code segment, and passing in the initial board configuration. The Solver then checks if the given board adheres to the constraints, returning a 9x9 matrix of `-1`'s if it does not. It then also evaluates whether the given board is a complete and consistent assignment (i.e. if it is already solved) and returns the corresponding output.
1. After the initial checks, the possible moves for each position of the board are initialized through `init_constraints`. This function iterates through each variable, defining its domain, based on the problem's constraints. This process is computationally expensive and as such is only called once per Sudoku board. To update the possible moves for an assignment later on in the algorithm, the possible moves of the previous state are copied over and updated. This approach proved particularly effective in optimizing the performance of the algorithm.
1. Once the possible values for each variable have been initialized, the `depth_first_search` function is called. This function implements the algorithm explained previously, combining a depth-first search and constraint propagation. It utilizes two heuristics for variable ordering, namely the *minimum-remaining-values* and *degree* heuristics. Both of these heuristics are explained further in the *Heuristics* sub-section below. After each call, the function decides which position to fill next and begins evaluating the possible outcomes. If any assignment is not consistent, the algorithm backtracks to the last known consistent assignment and tries a different path. To explore a given state further, the function makes a recursive call, repeating this process until an inconsistent state or solution is encountered. To create a new board state, the function uses the `gen_next_state` function of the `SudokuState` class.
1. The `gen_next_state` function efficiently creates a copy of the current `SudokuState` object, assigns a value to the variable in question, and uses the `update_constraints` function to propagate the constraints for the resulting board (i.e. updates all possible moves for the empty positions affected by the assignment). At this point, the function does an additional check to detect any singleton positions in the board, through `get_singletons`. This function finds any empty positions that have only one possible value, following the recent assignment, and returns them. These positions are then assigned their unique possible value. Finally, the resulting `SudokuState` object is returned to the `depth_first_search` function and is evaluated.

### Heuristics
The Solver utilizes two heuristics for variable ordering, i.e. choosing which empty position to fill next. These are the **minimum-remaining-values** (MRV) and **degree** heuristics. Their respective functions are invoked by the `pick_next` function in the driver code segment. By adding these heuristics and replacing the previous static variable ordering, the runtime of the solution improved greatly.

#### Minimum-remaining-values (MRV)  Heuristic
The minimum-remaining-values heuristic, also called the "most constrained variable" heuristic, picks the variable with the fewest possible values. [2] In doing so, it picks the variable that has the highest likelihood of resulting in failure soon, reducing the number of computations otherwise spent searching other variables first. By extent, if a variable has no possible values left, then it would be selected and result in failure straight away. It is implemented in the `get_min_value_positions` function. Note that multiple variables can have the same number of possible values, and as such the MRV heuristic may return a list of variables. In this case, the *degree* heuristic is used as a tie-breaker. 

#### Degree Heuristic
The degree heuristic selects the variable with the most constraints on other unassigned variables, i.e. the one that affects the greatest number of empty positions. [2] It is used when the MRV heuristic returns multiple variables, to decide which position should be picked, instead of using static variable ordering. The degree heuristic is split among two functions; the `pick_next` and `get_degree` functions. The latter calculates the "degree" of each position (i.e. the number of other empty positions it affects), while the `pick_next` function finds the variable with the maximum degree and returns it.

## Results and Discussion
### Results
Prior to including the heuristics in the solution, the solver would use static variable ordering which does not typically result in an efficient search. [2] By including variable ordering heuristics, the overall runtime of the solution improved drastically. This is because, thanks to the heuristics, the variable that is most likely to result in failure is assigned first. The greatest change in performance was noticed when the minimum-remaining-values heuristic was added to the solution. However, by pairing MRV with the degree heuristic, the runtime significantly improved once more, resulting in a total runtime of 5.1 - 6.2 second for all tests.

### Code Optimization
In order for the agent to be able to solve hard Sudoku puzzles in a small timeframe, the implementation had to be optimized. In this capacity, the choice of data structures and algorithms used in the Solver was a key area that had to be explored. Through a mixture of trial-and-error, research, and capitalizing on the technical details of the problem the Solver was optimized and was able to solve all test puzzles in a short amount of time. A brief description of some areas that were explored follows:

Multi-dimensional `numpy` arrays were chosen as the main data structure to store information in the solution. By using a universal data type throughout the solution, the computational costs associated with conversions from one data type to another are avoided. `numpy` arrays were chosen over other alternatives, like python's `list` objects, as they provide in-built functions to iterate and manipulate their contents efficiently, like `ndenumarate`, `ndindex` and `full`. Additionally, the library provides a way of importing Sudoku puzzles from external files directly into a `numpy` array without the need of complex, expensive operations, aiding both code clarity and efficiency.

Other data structures like `dictionaries` and `lists` are also used in certain parts of the solution, namely in the heuristic functions. These however, do not alter the representation of the Sudoku board (`SudokuState`) and are solely used in the functions to improve time complexity at the cost of space complexity.

Previous iterations of the Solver made use of the `deepcopy` function from the `copy` library, when creating a copy of the `SudokuState` object.Through time analysis of the solution, via a code profiler, the `deepcopy` was proven to take up over 78% of the solution's runtime. To overcome the overheads associated with it, the implementation includes the `copy_state` function which is capable of creating a copy of a `SudokuState` object more efficiently. Additionally, the number of function calls of `copy_state` were significantly reduced, by assigning singleton cells and propagating the constraints as soon as they are detected, without needing to create an additional copy of the board.

### Future Work
The current implementation of the Solver, makes use of two heuristic functions for selecting which variable to pick next. It lacks however a heuristic for value ordering, i.e. the order in which it will try to assign values to a given variable. At the moment, after selecting a variable to explore further, the Solver begins assigning values sequentially. The *least-constraining-value* heuristic should be considered as an improvement to the current implementation, as it may result in faster runtimes. This heuristic picks the value that rules out the least number of choices for other variables. [2] Before incorporating it in the solution however, further research should be conducted, as it is possible that an unoptimized implementation of this heuristic may result in an increase in overall runtime, rather than a decrease.

Apart from a constraint satisfaction problem, Sudoku can also be represented as an exact cover problem. Exact cover problems are decision problems which can be represented by a set and a collection of its subsets. Knuth's *Algorithm X* is capable of solving exact cover problems and if implemented correctly using *Dancing links* is a very efficient approach. [3] As further work, this approach should be explored in more depth, implemented and compared with the current solution.

Multi-threading was beyond the scope of this project and as such was not included in the current implementation. However, it poses an area for further research, as by successfully incorporating multi-threading in the solution, the overall runtime of the Solver would improve.

## References
[1] Rossi, F., 2006. *Handbook of constraint programming*. Amsterdam: Elsevier.

[2] Norvig, P., Russel, S., 2016. *Artificial Intelligence: A Modern Approach*. Third Edition. Harlow: Pearson Education.

[3] Knuth, D. E., 2000. *Dancing links* [Online]. Stanford: University of Stanford. Available from: https://arxiv.org/pdf/cs/0011047.pdf [Accessed 14 June 2021].
