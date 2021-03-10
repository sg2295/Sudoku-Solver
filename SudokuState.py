import copy
import numpy as np


class SudokuState:
    def __init__(self, final_values):
        self.final_values = final_values.copy()
        self.possible_values = self.__generate_possible_values()
        print(self.possible_values)

    def __generate_possible_values(self):
        possible_values = [[[] for _ in range(9)] for _ in range(9)]

        for (row, col), curr_value in np.ndenumerate(self.final_values):
            if curr_value == 0:
                for value in range(1, 10):
                    if self.__is_valid(row, col, value):
                        possible_values[row][col].append(value)

        return possible_values

    def __is_valid(self, target_row, target_col, value):
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
