import SudokuState
import numpy as np


def get_minimum_value_pos(sudoku_state):
    """
    Finds the most constrained value, then finds all positions that have the same constrain value
    # todo comments + docstring + dictionary O(n) + O(1) instead of O(2n)
    """
    min_row, min_col, curr_min = -1, -1, 9  # Assume most constrained position has 9 possible moves (max num of moves)
    for (row, col), values in np.ndenumerate(sudoku_state.possible_values):
        if 0 < len(values) < curr_min:  # Check if the current variable is more constrained (less possible moves)
            min_row, min_col = row, col
            curr_min = len(values)  # Update current minimum number of moves

    mrv_positions = []  # Todo: can make this with 1 loop if i use dictionary/hashmap
    for (row, col), values in np.ndenumerate(sudoku_state.possible_values):
        if len(values) == curr_min:
            mrv_positions.append((row, col))

    return mrv_positions


def get_constrain_number(sudoku_state, row, col):
    """
    Finds the number of empty positions affecting the element todo: docstring + comments

    """
    counter = 0
    for i in range(9):
        if sudoku_state.final_values[row][i] == 0 and i != col:
            counter += 1
        if sudoku_state.final_values[i][col] == 0 and i != row:
            counter += 1

    # Find start of 3x3 block:
    block_row = row - (row % 3)
    block_col = col - (col % 3)

    # Check each element in the 3x3 block:
    for temp_row in range(3):
        for temp_col in range(3):
            if sudoku_state.final_values[temp_row + block_row][temp_col + block_col] and temp_row + block_row != row and temp_col + block_col != col:
                counter += 1

    return counter


def pick_next_cell(sudoku_state):
    """
    # Todo fix comments + doc string
    Find the most constrained variable (value), i.e. the vacant position with the least possible values.
    Applies the minimum-remaining-values (MRV) heuristic. Iterates through each position and finds the position that is
    the most constrained (i.e. has the least possible moves).
    :param sudoku_state: The sudoku state to apply the heuristic to (SudokuState Object).
    :return: The position (row, col) of the most constrained value.
    """
    """
    Find the position which is affected by the most number of other empty cells (use MRV and max degree heuristic)
    """
    minimum_value_positions = get_minimum_value_pos(sudoku_state)
    max_row, max_col = -1, -1
    max = 0
    for position in minimum_value_positions:
        curr = get_constrain_number(sudoku_state, position[0], position[1])
        if curr > max:
            max = curr
            max_row, max_col = position
    return max_row, max_col


def depth_first_search(sudoku_state):
    """
    TODO Write up docstring
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
