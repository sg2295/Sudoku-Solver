import copy
import numpy as np


class SudokuState:
    def __init__(self, final_values):
        """
        Creates a SudokuState Object following the given board specifications.
        :param final_values: The board configuration. Two dimensional (2d) numpy array with values in range (0, 9).
        """
        self.final_values = final_values  # Holds the final values on the board
        self.possible_values = np.empty(shape=(9, 9), dtype=list)  # Holds the possible values each empty slot can take

    def init_constraints(self):
        """
        Go through all empty positions and initialize their possible values, according to the constraints.
        Called once when the board is first created.
        :return: None
        """
        for (row, col), curr_value in np.ndenumerate(self.final_values):
            self.possible_values[row][col] = []  # Initialize empty list
            if curr_value == 0:  # If the final value is 0 then the position is vacant
                for value in range(1, 10):  # Iterate through all possible values (1, 9) and check if they are possible
                    if self.__is_valid_value(row, col, value):
                        self.possible_values[row][col].append(value)  # Append possible values to the corresponding list
        return

    def __is_valid_value(self, target_row, target_col, value):
        """
        Check if the given value is allowed to be placed in the specified position (target_row, target_col).
        Checks that no duplicate values are in the same row, column or 3x3 block.
        :param target_row: The row position where the value will be placed.
        :param target_col: The column position where the value will be placed.
        :param value: The value that is being evaluated.
        :return: True if it is a possible (valid) value, False otherwise.
        """
        if value == 0:
            return True  # 0's are always a valid value since they are a placeholder (signify empty position)

        # Check row and column:
        for i in range(9):
            if self.final_values[i][target_col] == value and i != target_row:  # Check column
                return False  # Value appears on the same column twice
            if self.final_values[target_row][i] == value and i != target_col:  # Check row
                return False  # Value appears on the same row twice

        # Find start of 3x3 block:
        block_row = target_row - (target_row % 3)
        block_col = target_col - (target_col % 3)

        # Check each element in the 3x3 block:
        for row in range(3):
            for col in range(3):
                if value == self.final_values[block_row + row][block_col + col] and block_row + row != target_row and block_col + col != target_col:
                    return False  # Value appears in the same block

        return True  # Value does not appear in the same row, col or block

    def is_valid_board(self):
        """
        Checks whether the given board is a valid sudoku board. (No duplicates on row, col or block).
        Iterate through every position in the board and check if it is a valid (possible) value, i.e. no duplicates in
        the same row, column or 3x3 block.
        :return: True if it is valid board, False otherwise.
        """
        for (row, col), value in np.ndenumerate(self.final_values):  # Iterate through each position
            if not self.__is_valid_value(row, col, value):  # Check that the value is valid
                return False  # An invalid (duplicate) value was found
        return True

    def is_solvable(self):
        """
        Checks if the board is solvable, i.e. each empty position has at least one possible value.
        :return: True if the board is solvable
        """
        for (row, col), value in np.ndenumerate(self.final_values):
            if value == 0 and len(self.possible_values[row][col]) < 1:
                return False
        return True

    def is_goal(self):
        """
        :return: True if every position has a value (no zeroes in the state), otherwise False
        """
        if 0 in self.final_values:
            return False
        return True

    def get_singletons(self):
        """
        Generates a list with the coordinates of all the empty slots that have only 1 possible value (singletons).
        Called after assignment (generate of new board).
        :return: List with the coordinates of all the singleton values.
        """
        singletons = []
        for row in range(9):
            for col in range(9):
                if len(self.possible_values[row][col]) == 1 and self.final_values[row][col] == 0:
                    singletons.append([row, col])
        return singletons

    def update_constraints(self, target_row, target_col, value):
        """
        Update the possible values, following an assignment to the given position (row, col).
        Find and update the affected positions, applying the constraints.
        """
        for i in range(9):
            if value in self.possible_values[target_row][i]:  # checks the horizontal
                self.possible_values[target_row][i].remove(value)
            if value in self.possible_values[i][target_col]:  # checks the vertical
                self.possible_values[i][target_col].remove(value)

        # checks the box
        block_row = target_row - (target_row % 3)
        block_col = target_col - (target_col % 3)
        for row in range(3):
            for col in range(3):
                if value in self.possible_values[block_row + row][block_col + col]:
                    self.possible_values[block_row + row][block_col + col].remove(value)

    def gen_next_state(self, row, col, value):
        """
        Generates the board configuration after we place the given value in position (row, col). Places the value in
        the specified position, iterates through the affected positions and updates their constraints.
        :return:
        """
        state = copy.deepcopy(self)  # Create a copy of the current state (board)
        # Update the board configuration:
        state.final_values[row][col] = value
        state.possible_values[row][col] = []

        state.update_constraints(row, col, value)  # Update affected possible values (apply constraints)

        singleton_list = state.get_singletons()  # Find singletons for this board configuration
        while singleton_list:
            row, col = singleton_list[0]
            state = state.gen_next_state(row, col, state.possible_values[row][col][0])  # Generate new state
            singleton_list = state.get_singletons()  # Get the remaining singletons

        return state
