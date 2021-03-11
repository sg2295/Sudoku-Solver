import copy
import numpy as np


class SudokuState:
    def __init__(self, final_values):
        self.final_values = final_values.copy()
        self.possible_values = self.__generate_possible_values()

    def __generate_possible_values(self):
        possible_values = np.empty(shape=(9, 9), dtype=object)
        for (row, col), curr_value in np.ndenumerate(self.final_values):
            possible_values[row][col] = []
            if curr_value == 0:
                for value in range(1, 10):
                    if self.__is_valid_value(row, col, value):
                        possible_values[row][col].append(value)

        return possible_values

    def __is_valid_value(self, target_row, target_col, value):
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

        return True

    def get_final_values(self):
        if self.is_goal():
            return self.final_values.copy()
        return np.full(shape=(9, 9), fill_value=-1, dtype=int)

    def is_goal(self):
        if 0 in self.final_values:
            return False
        return True

    def is_invalid(self):
        for (row, col), value in np.ndenumerate(self.final_values):
            if not self.__is_valid_value(row, col, value):
                return True
        return False

    def is_solvable(self):
        for (row, col), value in np.ndenumerate(self.final_values):  # Check that each empty slot has a possible value:
            if value == 0 and len(self.possible_values[row][col]) == 0:
                return False
        return True

    def get_singleton(self):
        for (row, col), value in np.ndenumerate(self.possible_values):
            if len(value) == 1:
                return (row, col), value[0]
        return None

    # def __deepcopy__(self, memodict={}):
    #
    #     pass

    def gen_next_state(self, row, col, value):
        new_state = copy.deepcopy(self)
        new_state.final_values[row][col] = value
        new_state.possible_values = new_state.__generate_possible_values()
        singleton = new_state.get_singleton()
        if singleton:
            new_state = new_state.gen_next_state(singleton[0][0], singleton[0][1], singleton[1])
            # singleton = new_state.get_singleton()
        return new_state
