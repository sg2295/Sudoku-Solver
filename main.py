import SudokuState
import numpy as np


def pick_next_cell(sudoku):
    """
    Find the most constrained value, i.e. the vacant position with the least possible values.
    :param sudoku:
    :return:
    """
    min_row, min_col, curr_min = -1, -1, 9  # Assume minimum
    for (row, col), values in np.ndenumerate(sudoku.possible_values):
        if 0 < len(values) < curr_min:
            min_row, min_col = row, col
            curr_min = len(values)
            if curr_min == 1:  # If it is a singleton, return it immediately
                break
    return min_row, min_col


def depth_first_search(state):
    row, col = pick_next_cell(state)
    values = state.possible_values[row][col]

    for value in values:
        new_state = state.gen_next_state(row, col, value)
        if new_state.is_goal():
            return new_state
        if not new_state.is_invalid():
            deep_state = depth_first_search(new_state)
            if deep_state is not None and deep_state.is_goal():
                return deep_state

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
    """
    solved = SudokuState.SudokuState(sudoku)
    if not solved.is_valid_board():
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)
    solved.init_constraints()
    solved = depth_first_search(solved)
    if solved is None:
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)
    return solved.final_values
