import copy
import numpy as np


class SudokuState:
    def __init__(self, final_values):
        self.final_values = final_values.copy()
        self.possible_values = np.empty(shape=(9, 9), dtype=object)

    def generate_possible_values(self):
        # Initialize the possible values with valid combinations
        for (row, col), curr_value in np.ndenumerate(self.final_values):
            self.possible_values[row][col] = []
            if curr_value == 0:
                for value in range(1, 10):
                    if self.__is_valid_value(row, col, value):
                        self.possible_values[row][col].append(value)

    def update_possible_values(self, target_row, target_col, value):
        # Update the possible values, after placing the given value in position (target_row, target_col)
        for i in range(9):
            if value in self.possible_values[i][target_col]:  # Update the column
                self.possible_values[i][target_col].remove(value)
            if value in self.possible_values[target_row][i]:  # Update the row
                self.possible_values[target_row][i].remove(value)

        # Find start of 3x3 block:
        block_row = target_row - (target_row % 3)  # Get the starting row
        block_col = target_col - (target_col % 3)  # Get the starting column

        # Update each element in the 3x3 block:
        for row in range(3):
            for col in range(3):
                if value in self.possible_values[block_row + row][block_col + col]:
                    self.possible_values[block_row + row][block_col + col].remove(value)

        return

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
        # Check that each value (apart from 0) appears only once per row, col, block
        for (row, col), value in np.ndenumerate(self.final_values):
            if not self.__is_valid_value(row, col, value):
                return True
        return False

    def is_solvable(self):
        for (row, col), value in np.ndenumerate(self.final_values):  # Check that each empty slot has a possible value:
            if value == 0 and len(self.possible_values[row][col]) == 0:
                return False
        return True

    def get_singletons(self):
        singleton_cells = []
        for (row, col), value in np.ndenumerate(self.possible_values):
            if len(value) == 1 and self.final_values[row][col] == 0:
                singleton_cells.append(((row, col), value[0]))
        return singleton_cells

    # def __deepcopy__(self, memodict={}):
    #
    #     pass

    def gen_next_state(self, row, col, value):
        new_state = copy.deepcopy(self)
        new_state.final_values[row][col] = value
        new_state.update_possible_values(row, col, value)

        singletons = new_state.get_singletons()
        while len(singletons) > 0:
            new_state = new_state.gen_next_state(singletons[0][0][0], singletons[0][0][1], singletons[0][1])
            singletons = new_state.get_singletons()
        return new_state
