import SudokuState
import numpy as np


def pick_next(sudoku):
    """
    Find the most constrained position!!
    :param sudoku:
    :return:
    """
    # Choose a value to change (return row, col)
    # Pick the slot with the MOST constraints/least possible values
    # least constrain, but watch out this doesn't end up adding more complexity than it saves
    min_row, min_col, min_len = -1, -1, 10
    for (row, col), value in np.ndenumerate(sudoku.possible_values):
        if 0 < len(value) < min_len:
            min_row, min_col = row, col
            min_len = len(value)
            if min_len == 1:
                break

    return min_row, min_col


def depth_first_search(sudoku):
    row, col = pick_next(sudoku)
    values = sudoku.possible_values[row][col]

    for value in values:
        new_sudoku = sudoku.gen_next_state(row, col, value)
        if new_sudoku.is_goal():
            sudoku = new_sudoku
            break
        if new_sudoku.is_solvable():
            deep_sudoku = depth_first_search(new_sudoku)
            if deep_sudoku.is_goal():
                sudoku = deep_sudoku
                break

    return sudoku


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
    solved.generate_possible_values()
    if not solved.is_invalid():
        solved = depth_first_search(solved)
    return solved.get_final_values()


# def depth_first_search(sudoku):
#     if sudoku.is_invalid() or not sudoku.is_solvable():
#         return sudoku
#
#     row, col = pick_next(sudoku)
#     # if row == -1 or col == -1:
#     #     return sudoku
#
#     values = sudoku.possible_values[row][col]
#
#     for value in values:
#         new_sudoku = depth_first_search(sudoku.gen_next_state(row, col, value))
#         if new_sudoku.is_goal():
#             sudoku = new_sudoku
#             break
#
#     return sudoku
