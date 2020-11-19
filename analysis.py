#This will generate a file with random puzzles
import random
from uniform_cost import uniform_cost
from puzzle import Puzzle
def analysis():

    puzzle_qty = 50
    fifty_puzzle_file = './a2-dataset/puzzles.txt'
    
    with open(fifty_puzzle_file, 'w')as f:
        template_puzzle = [1,2,3,4,5,6,7,0]
        for x in range(puzzle_qty):
            random.shuffle(template_puzzle)
            f.write(str(template_puzzle).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip() + '\n')
            
    f.close()

    total_length_solution =0
    total_length_search = 0
    total_nb_nosolution = 0
    total_cost_50 = 0
    total_execution_time = 0
    cols = 4
    rows = 2
    with open(fifty_puzzle_file) as file:
        for line in file:
            temp_puzzle = list(map(int ,line.split(' ')))
            puzzle = Puzzle(temp_puzzle, cols, rows)
            goal_node, total_cost, closedlist, execution_time = uniform_cost(puzzle)
            

            total_length_solution += len(goal_node.solution_path())
            total_length_search += len(closedlist)
            if execution_time >= 60:
                total_nb_nosolution += 1
            total_cost_50 += total_cost
            total_execution_time += execution_time
    file.close()

    avg_length_solution = total_length_solution/puzzle_qty
    avg_length_search = total_length_search/puzzle_qty
    avg_nb_nosolution = total_nb_nosolution/puzzle_qty
    avg_cost = total_cost/puzzle_qty
    avg_execution_time = total_execution_time/puzzle_qty

    with open('./output/ucs_analysis.txt', 'w') as f:
        f.write(f'Total length of search: {total_length_search}\n')
        f.write(f'Total length of solution: {total_length_solution}\n')
        f.write(f'Total number of no solution: {total_nb_nosolution}\n')
        f.write(f'Total cost: {total_cost}\n')
        f.write(f'Total execution time: {total_execution_time}\n')
        f.write(f'Average length of search: {avg_length_search}\n')
        f.write(f'Average length of solution: {avg_length_solution}\n')
        f.write(f'Average number of no solution: {avg_nb_nosolution}\n')
        f.write(f'Average cost: {avg_cost}\n')
        f.write(f'Average execution time: {avg_execution_time}\n')
    f.close()

analysis()


