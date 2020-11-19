#This will generate a file with random puzzles
import random
from uniform_cost import uniform_cost
from puzzle import Puzzle
from write_functions import write_analysis
def analysis():

    puzzle_qty = 50
    fifty_puzzle_file = './a2-dataset/puzzles.txt'
    output_directory = './output'

    with open(fifty_puzzle_file, 'w')as f:
        template_puzzle = [1,2,3,4,5,6,7,0]
        for x in range(puzzle_qty):
            random.shuffle(template_puzzle)
            f.write(str(template_puzzle).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip() + '\n')  
    f.close()

    cols = 4
    rows = 2

    ###################################
    #######        UCS          #######
    ###################################

    #write_analysis(output_directory, fifty_puzzle_file, 'ucs', cols, rows, puzzle_qty)

    ###################################
    #######        GBFS         #######
    ###################################

    #write_analysis(output_directory, fifty_puzzle_file, 'gbfs', cols, rows, puzzle_qty, heuristic = 'h0')
    write_analysis(output_directory, fifty_puzzle_file, 'gbfs', cols, rows, puzzle_qty, heuristic = 'h1')
    write_analysis(output_directory, fifty_puzzle_file, 'gbfs', cols, rows, puzzle_qty, heuristic = 'h2')

    ###################################
    #######        A*           #######
    ###################################

    #write_analysis(output_directory, fifty_puzzle_file, 'astar', cols, rows, puzzle_qty, heuristic = 'h0')
    write_analysis(output_directory, fifty_puzzle_file, 'astar', cols, rows, puzzle_qty, heuristic = 'h1')
    write_analysis(output_directory, fifty_puzzle_file, 'astar', cols, rows, puzzle_qty, heuristic = 'h2')
analysis()