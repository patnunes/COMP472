import time
from uniform_cost import uniform_cost
from puzzle import Puzzle
from write_functions import write_solution, write_search


def main():

    puzzle3 = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 4, 2)

    start = time.time()
    goal_node, total_cost, closedlist = uniform_cost(puzzle3)
    
    end = time.time()
    execution_time = end - start
    print(execution_time)

    output_directory = './output'

    write_solution(output_directory, execution_time, goal_node, total_cost, 'ucs')
    write_search(output_directory, closedlist, 'ucs')


main()
