import copy
import numpy as np


class SudokuState:
    def __init__(self, sudoku):
        self.final_values = sudoku.copy()
        self.possible_values = self.__generate_possible_values()

    def __generate_possible_values(self):
        """
        Generates all the possible values (moves) for a given board. Iterates thru each point and finds it's possible
        values.
        Called in the constructor.

        """
        possible_values = np.empty(shape=(9, 9), dtype=object)  # 2-d numpy array holding a list of possible values
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Holds all possible values

        # Find all zeroes and see what values we can place in them
        for row in range(9):
            for col in range(9):
                possible_values[row][col] = []
                if self.final_values[row][col] == 0:  # Empty slot
                    for value in range(1, 10):  # Test all possible values 1 --> 9
                        if self.__is_possible_value(row, col, value):
                            possible_values[row][col].append(value)  # If the value is possible add it to the list

        return possible_values

    def __is_possible_value(self, target_row, target_col, value):
        """
        Checks if the given value is valid for the given position (targer_row, target_col).
        Called in __generate_possible_values, is_invalid, set_value
        """
        if value == 0:
            return True  # If given a 0, return True (it is a placeholder)

        for i in range(9):  # Check that the value appears once in the row and column
            if self.final_values[i][target_col] == value and i != target_row:  # Check the column
                return False
            if self.final_values[target_row][i] == value and i != target_col:  # Check the row
                return False

        # Find start of 3x3 block:
        block_row = target_row - (target_row % 3)  # Get the starting row
        block_col = target_col - (target_col % 3)  # Get the starting column

        # Iterate thru each element in the 3x3 block:
        for row in range(3):
            for col in range(3):
                if self.final_values[row + block_row][col + block_col] == value:
                    if row + block_row != target_row and col + block_col != target_col:
                        return False

        return True  # Value does not appear on the same row, col or 3x3 block

    def is_goal(self):
        """
        Checks if the given board is a goal state (no 0). Returns True/False.
        Called in get_final_state
        """
        if 0 in self.final_values:
            return False
        return True

    def is_invalid(self):
        """
        Check that the current board is a valid board configuration.
        """
        for row in range(9):
            for col in range(9):
                if not self.__is_possible_value(row, col, self.final_values[row][col]):
                    return True
        return False

    def get_possible_values(self, row, col):
        """
        Returns a copy of all the possible values
        """
        return self.possible_values[row][col].copy()

    def get_final_state(self):
        """
        If it is a goal state, return the final values (result). Otherwise return a 9x9 numpy array of -1.
        """
        if self.is_goal():
            return self.final_values  # If it is a goal state, return the final values
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)  # If it is not a goal state, return -1's

    def get_singletons(self):
        """
        Return coordinates of positions that have only 1 possible value.
        """
        singleton_list = []
        # Iterate thru each point
        for row in range(9):
            for col in range(9):
                if self.final_values[row][col] == 0 and len(self.possible_values[row][col]) == 1:
                    singleton_list.append((row, col))  # Is an empty position + has 1 possible move
        return singleton_list

    def set_value(self, row, col, value):
        """
        Sets the given value to the row, col position
        """
        if not self.__is_possible_value(row, col, value):
            return None

        state = copy.deepcopy(self)  # Create a copy of the current state
        state.final_values[row][col] = value

        # Update all other positions.
        # Start with row/column
        for i in range(9):
            if value in state.possible_values[i][col]:  # Remove from column
                state.possible_values[i][col].remove(value)
            if value in state.possible_values[row][i]:  # Remove from row
                state.possible_values[row][i].remove(value)

        # Find start of 3x3 block:
        block_row = row - (row % 3)  # Get the starting row
        block_col = col - (col % 3)  # Get the starting column

        for target_row in range(3):
            for target_col in range(3):
                if value in state.possible_values[block_row + target_row][block_col + target_col]:
                    state.possible_values[block_row + target_row][block_col + target_col].remove(value)

        # Find any other places with only one value and add these here
        singleton_list = state.get_singletons()
        while len(singleton_list):
            new_row, new_col = singleton_list[0]
            state = state.set_value(new_row, new_col, state.possible_values[new_row][new_col][0])
            singleton_list = state.get_singletons()

        return state
