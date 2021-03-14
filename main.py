import SudokuState
import numpy as np


def get_min_value_positions(sudoku_state):
    """
    Finds the minimum remaining values for any state in the board, and then finds all positions that have the same
    number of values, i.e. all the states that have the minimum number of remaining values.
    :param sudoku_state: The sudoku state to apply the heuristic to (SudokuState Object).
    :return: A list of the positions with the minimum remaining values.
    """
    position_choices = {}  # Holds list of positions (value) for each number 0 - 9 (key)
    for key in range(9):  # Populate dictionary with empty lists
        position_choices[key] = []

    for (row, col), values in np.ndenumerate(sudoku_state.possible_values):
        position_choices[len(values)].append((row, col))  # Iterate through each empty position and add to dict

    # Find the position(s) with the minimum possible moves
    for i in range(1, 9):
        if position_choices[i]:
            return position_choices[i]  # Return the list with the least remaining values


def get_degree(sudoku_state, row, col):
    """
    Finds the number of empty positions affecting the element, i.e. the empty positions on the same row, column
    and block. Used for the degree heuristic.
    :param sudoku_state: The sudoku state to evaluate (SudokuState Object).
    :param row: The row of the position to be evaluated.
    :param col: The column of the position to be evaluated.
    :return: The given position's degree (the number of empty positions on the same row, column and block).
    """
    degree_counter = 0  # Holds the number of empty positions on the same row, column and block
    for i in range(9):
        if sudoku_state.final_values[row][i] == 0:  # Search the column
            degree_counter += 1
        if sudoku_state.final_values[i][col] == 0:  # Search the row
            degree_counter += 1

    # Find start of 3x3 block:
    block_row = row - (row % 3)
    block_col = col - (col % 3)

    # Check each element in the 3x3 block:
    for temp_row in range(3):
        for temp_col in range(3):
            if sudoku_state.final_values[temp_row + block_row][temp_col + block_col]:  # Empty position in block
                degree_counter += 1

    return degree_counter  # Return the number of positions affected by the current position


def pick_next_cell(sudoku_state):
    """
    Apply the minimum-remaining-values (MRV) heuristic, then the degree heuristic to find the most suitable move.
    By combining these two heuristics we have a higher likelihood of resulting in an invalid board configuration faster,
    significantly improving runtime.
    Minimum-remaining-values heuristic --> finds the position(s) with the least possible remaining moves.
    Degree heuristic --> finds the position that affects (and is affected by) the maximum number of empty positions.
    :param sudoku_state: The sudoku state to apply the heuristics to (SudokuState Object).
    :return: The position (row, col) of the most constrained value.
    """
    # Use the minimum-remaining values heuristic:
    min_value_positions = get_min_value_positions(sudoku_state)  # Get the positions (row, col) with the minimum moves
    # Use the degree heuristic:
    max_row, max_col, max_degree = -1, -1, 0  # Assume the highest degree is 0 at first
    for position in min_value_positions:  # Loop through all of the minimum-remaining-values positions
        curr_degree = get_degree(sudoku_state, position[0], position[1])  # Get the degree for the position
        if curr_degree > max_degree:
            max_degree = curr_degree  # If the current degree is higher than the max, update the max
            max_row, max_col = position
    return max_row, max_col  # Return the coordinates of the position with the highest degree


def depth_first_search(sudoku_state):
    """
    Uses the depth-first search (DFS) algorithm to find a solution (if it exists) to the given Sudoku board.
    Makes use of the minimum-remaining-value (MRV) and degree heuristics to find a solution to the given board, if
    a solution exists. After selecting a position to fill, it creates a new SudokuState object for each possible value
    of the current position. It then recursively calls itself until it finds the solution, or an invalid state,
    backtracking if needed. Uses forward checking to identify dead-ends without going "deep".
    :param sudoku_state: Sudoku board configuration to be evaluated (SudokuState object).
    :return: The SudokuState representing the solved board, or None (indicating it is not solvable).
    """
    row, col = pick_next_cell(sudoku_state)  # Pick position for next move
    values = sudoku_state.possible_values[row][col]

    for value in values:  # For each possible value
        new_state = sudoku_state.gen_next_state(row, col, value)  # Generate the resulting board
        if new_state.is_goal():
            return new_state  # If it is a goal state return it
        if new_state.is_solvable():
            deep_state = depth_first_search(new_state)
            if deep_state and deep_state.is_goal():
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

    solved.init_constraints()  # Generate the initial possible values
    solved = depth_first_search(solved)  # Attempt to solve the board using depth-first search

    if not solved:
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)  # Return 9x9 matrix of -1s if it has no solution

    return solved.final_values  # Return the final sudoku board configuration
