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

    for (row, col), value in np.ndenumerate(sudoku.possible_values):
        if len(value) > 0:
            return row, col


def order_values(sudoku, row, col):
    # Get the possible values for a slot sorted in the order to try them in, could be left as random.
    return sudoku.get_possible_values(row, col)


def depth_first_search(sudoku):
    if sudoku.is_invalid() or not sudoku.is_solvable():
        return sudoku

    row, col = pick_next(sudoku)
    # if row == -1 or col == -1:
    #     return sudoku

    values = sudoku.possible_values[row][col]

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
