import SudokuState
import numpy as np


def pick_next(sudoku):
    # Choose a value to change (return row, col)
    # Pick the slot with the MOST constraints/least possible values
    # least constrain, but watch out this doesn't end up adding more complexity than it saves
    for row in range(9):
        for col in range(9):
            if len(sudoku.get_possible_values(row, col)) > 0:
                return row, col


def order_values(sudoku, row, col):
    # Get the possible values for a slot sorted in the order to try them in, could be left as random.
    return sudoku.get_possible_values(row, col)


def depth_first_search(sudoku):
    if sudoku.is_invalid() or sudoku.is_goal() or not sudoku.is_solvable():
        return sudoku

    row, col = pick_next(sudoku)
    values = order_values(sudoku, row, col)

    for value in values:
        new_sudoku = depth_first_search(sudoku.gen_next_state(row, col, value))
        if new_sudoku.is_goal():
            sudoku = new_sudoku
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
    return depth_first_search(solved).get_final_values()

# def depth_first_search(sudoku):
#     # Check valid
#     if sudoku.is_invalid():
#         return sudoku
#
#     # Does a DFS on the sudoku, trying each possible value for every position until it finds a solution
#     position = pick_next(sudoku)
#     if position is None:
#         return sudoku
#     row, col = position
#     values = order_values(sudoku, row, col)
#
#     for value in values:
#         new_state = sudoku.set_value(row, col, value)
#         if new_state is None:
#             break
#         if new_state.is_goal():
#             return new_state
#         if not new_state.is_invalid():
#             deep_state = depth_first_search(new_state)
#             if deep_state is not None and deep_state.is_goal():
#                 return deep_state
#     return sudoku
