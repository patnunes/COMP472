import time
from uniform_cost import uniform_cost
from puzzle import Puzzle
from write_functions import write_solution, write_search_path


def main():

    puzzle3 = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 4, 2)

    start = time.time()
    goal_node, total_cost = uniform_cost(puzzle3)
    end = time.time()
    execution_time = end - start
    print(execution_time)
    # #input_file = './output'
    output_directory = './output'

    # # uniform_cost(puzzle3)
    write_solution(output_directory, execution_time, goal_node, total_cost, 'ucs')
    # # write_search_path(output_directory, execution_time, solution_path, 'ucs')


main()
