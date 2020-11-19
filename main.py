import time
from uniform_cost import uniform_cost
from A_star import a_star
from greedys_best_first import best_first_search
from puzzle import Puzzle
from write_functions import write_solution, write_search


def main():

    input_file = './a2-dataset/samplePuzzles.txt'
    output_directory = './output'
    rows = 2
    cols = 4

    puzzle_ctr = -1
    temp_puzzle = []
    with open(input_file) as file:
        for line in file:
            temp_puzzle = list(map(int ,line.split(' ')))
            puzzle_ctr += 1
            print(temp_puzzle)
            puzzle = Puzzle(temp_puzzle, cols, rows)

            
            goal_node, total_cost, closedlist, execution_time = uniform_cost(puzzle)
            write_solution(puzzle_ctr ,output_directory, execution_time, goal_node, total_cost, 'ucs')
            write_search(puzzle_ctr , output_directory,execution_time, closedlist, 'ucs')

            goal_node, total_cost, closedlist, execution_time = best_first_search(puzzle, heuristic='h1')
            # write_solution(puzzle_ctr ,output_directory, execution_time, goal_node, total_cost, 'gbfs', 'h0' )
            # write_search(puzzle_ctr , output_directory,execution_time, closedlist, 'gbfs', 'h0')
            write_solution(puzzle_ctr ,output_directory, execution_time, goal_node, total_cost, 'gbfs', 'h1' )
            write_search(puzzle_ctr , output_directory,execution_time, closedlist, 'gbfs', 'h1')
            goal_node, total_cost, closedlist, execution_time = best_first_search(puzzle, heuristic='h2')
            write_solution(puzzle_ctr ,output_directory, execution_time, goal_node, total_cost, 'gbfs', 'h2' )
            write_search(puzzle_ctr , output_directory,execution_time, closedlist, 'gbfs', 'h2')

            goal_node, total_cost, closedlist, execution_time = a_star(puzzle, heuristic='h1')
            # write_solution(puzzle_ctr ,output_directory, execution_time, goal_node, total_cost, 'astar', 'h0' )
            # write_search(puzzle_ctr , output_directory,execution_time, closedlist, 'astar', 'h0')
            write_solution(puzzle_ctr ,output_directory, execution_time, goal_node, total_cost, 'astar', 'h1' )
            write_search(puzzle_ctr , output_directory,execution_time, closedlist, 'astar', 'h1')
            goal_node, total_cost, closedlist, execution_time = a_star(puzzle, heuristic='h2')
            write_solution(puzzle_ctr ,output_directory, execution_time, goal_node, total_cost, 'astar', 'h2' )
            write_search(puzzle_ctr , output_directory,execution_time, closedlist, 'astar', 'h2')
    file.close()

main()
