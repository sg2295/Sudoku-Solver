import main
import time
import numpy as np


# Provided testing code, from University of Bath

# Extra tests: https://www.kaggle.com/bryanpark/sudoku

def run_tests(difficulties=None):
    if difficulties is None:
        difficulties = ['very_easy', 'easy', 'medium', 'hard']

    very_start_time = time.process_time()
    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            start_time = time.process_time()
            your_solution = main.sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is: --------------------------------------------------------------")
                print(solutions[i])
                break

            print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break
    very_end_time = time.process_time()
    print("===========================\n")
    print("THE ENTIRE SOLUTION TAKES: ", very_end_time-very_start_time, " seconds")


def extra_tests():
    """
    Extra tests to make sure the current approach is indeed correct.
    :return:
    """
    quizzes = np.zeros((1000000, 81), np.int32)
    solutions = np.zeros((1000000, 81), np.int32)
    for i, line in enumerate(open('data/sudoku.csv', 'r').read().splitlines()[1:]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    print("Size: ", quizzes.size)
    input("okay?")
    puzzles_num = 10000
    times, count = 0, 0
    very_start_time = time.process_time()
    for quiz, solution in zip(quizzes[:puzzles_num], solutions[:puzzles_num]):

        # print(quiz)
        start_time = time.process_time()
        your_solution = main.sudoku_solver(quiz.copy())
        end_time = time.process_time()

        times += end_time-start_time
        count += 1
        # print(your_solution)
        if not np.array_equal(your_solution, solution):
            print("Wrong solution for: ", quiz)
            break
        # print("Time to solve: ", end_time-start_time, " seconds")

    very_end_time = time.process_time()
    print("===========================\n")
    print("THE ENTIRE SOLUTION TAKES: ", very_end_time-very_start_time, " seconds")
    print("===========================\n")
    print("Average solve time: ", times/count, " seconds")
    pass


if __name__ == "__main__":
    d = ["hard"]
    # run_tests(d)
    run_tests()
    # extra_tests()
    # s = np.full(shape=(9,9), fill_value=9, dtype=int)
    # solutions = np.load("data/very_easy_solution.npy")
    # print(main.sudoku_solver(solutions[0]))
    # print(main.sudoku_solver(s))
