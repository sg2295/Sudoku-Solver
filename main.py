import SudokuState
import numpy as np


def pick_next_cell(sudoku_state):
    """
    Find the most constrained variable (value), i.e. the vacant position with the least possible values.
    Applies the minimum-remaining-values (MRV) heuristic. Iterates through each position and finds the position that is
    the most constrained (i.e. has the least possible moves).
    :param sudoku_state: The sudoku state to apply the heuristic to (SudokuState Object).
    :return: The position (row, col) of the most constrained value.
    """
    min_row, min_col, curr_min = -1, -1, 9  # Assume most constrained position has 9 possible moves (max num of moves)
    for (row, col), values in np.ndenumerate(sudoku_state.possible_values):
        if 0 < len(values) < curr_min:  # Check if the current variable is more constrained (less possible moves)
            min_row, min_col = row, col
            curr_min = len(values)  # Update current minimum number of moves
            if curr_min == 1:  # If it is a singleton, return it immediately
                break
    return min_row, min_col


def depth_first_search(sudoku_state):
    """
    TODO Write up
    :param sudoku_state:
    :return:
    """
    row, col = pick_next_cell(sudoku_state)
    values = sudoku_state.possible_values[row][col]

    for value in values:  # For each possible value
        new_state = sudoku_state.gen_next_state(row, col, value)  # Generate the resulting board
        if new_state.is_goal():
            return new_state  # If it is a goal state return it
        if new_state.is_solvable():
            deep_state = depth_first_search(new_state)
            if deep_state is not None and deep_state.is_goal():
                return deep_state  # If it is a goal state return it

    return None


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.

    :param sudoku:
    :return:
    """
    solved = SudokuState.SudokuState(sudoku)
    if not solved.is_valid_board():  # Check that the board is a valid configuration (contains unique values).
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)  # Return 9x9 matrix of -1s if it is not solvable

    solved.init_constraints()  # Create initial
    solved = depth_first_search(solved)

    if solved is None:
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)  # Return 9x9 matrix of -1s if it has no solution

    return solved.final_values  # Return the final sudoku board configuration
