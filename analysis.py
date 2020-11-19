#This will generate a file with random puzzles
import random
from uniform_cost import uniform_cost
from puzzle import Puzzle
from write_functions import write_analysis
def analysis():

    puzzle_qty = 50
    fifty_puzzle_file = './a2-dataset/puzzles.txt'
    scaled_puzzle_file1 = './a2-dataset/scaled_puzzles1.txt'
    scaled_puzzle_file2 = './a2-dataset/scaled_puzzles2.txt'
    scaled_puzzle_file3 = './a2-dataset/scaled_puzzles3.txt'
    
    output_directory = './analysis_output'

    with open(fifty_puzzle_file, 'w') as f:
        template_puzzle = [1,2,3,4,5,6,7,0]
        for x in range(puzzle_qty):
            random.shuffle(template_puzzle)
            f.write(str(template_puzzle).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip() + '\n')  
    f.close()

    with open(scaled_puzzle_file1, 'w') as f:
        template_puzzle = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,0]
        for x in range(5):
            random.shuffle(template_puzzle)
            f.write(str(template_puzzle).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip() + '\n')  
    f.close()

    with open(scaled_puzzle_file2, 'w') as f:
        template_puzzle = [1,2,3,4,5,6,7,8,0]
        for x in range(5):
            random.shuffle(template_puzzle)
            f.write(str(template_puzzle).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip() + '\n')  
    f.close()

    with open(scaled_puzzle_file3, 'w') as f:
        template_puzzle = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
        for x in range(5):
            random.shuffle(template_puzzle)
            f.write(str(template_puzzle).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip() + '\n')  
    f.close()



    

    ###################################
    #######        UCS          #######
    ###################################
    
    #write_analysis(output_directory, fifty_puzzle_file, 'ucs', 4, 2, puzzle_qty)

    ###################################
    #######        GBFS         #######
    ###################################

    # write_analysis(output_directory, fifty_puzzle_file, 'gbfs', 4, 2, puzzle_qty, heuristic = 'h0')
    # write_analysis(output_directory, fifty_puzzle_file, 'gbfs', 3, 3, puzzle_qty, heuristic = 'h1')
    # write_analysis(output_directory, fifty_puzzle_file, 'gbfs', 4, 3, puzzle_qty, heuristic = 'h2')

    ##Scaled Up GBFS

    write_analysis(output_directory, scaled_puzzle_file1, 'gbfs', 5, 3, 5, heuristic = 'h1', restrict_time=False, ctr = '3x5')
    write_analysis(output_directory, scaled_puzzle_file2, 'gbfs', 3, 3, 5, heuristic = 'h1', restrict_time=False, ctr = '3x3')
    write_analysis(output_directory, scaled_puzzle_file3, 'gbfs', 4, 4, 5, heuristic = 'h1', restrict_time=False, ctr = '4x4')

    ###################################
    #######        A*           #######
    ###################################

    # write_analysis(output_directory, fifty_puzzle_file, 'astar', 4, 2, puzzle_qty, heuristic = 'h0')
    # write_analysis(output_directory, fifty_puzzle_file, 'astar', 4, 2, puzzle_qty, heuristic = 'h1')
    # write_analysis(output_directory, fifty_puzzle_file, 'astar', 4, 2, puzzle_qty, heuristic = 'h2')

analysis()