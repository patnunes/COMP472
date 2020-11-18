#This will generate a file with random puzzles
import random
#sample = './a2-dataset/samplePuzzles.txt'
puzzle_file = './a2-dataset/puzzles.txt'
puzzles = []
with open(puzzle_file, 'w')as f:
    template_puzzle = [1,2,3,4,5,6,7,0]
    for x in range(50):
        random.shuffle(template_puzzle)
        f.write(str(template_puzzle) + '\n')
        puzzles.append(template_puzzle)

total_length_solution =0
total_length_search = 0
total_nb_nosolution = 0
total_cost = 0
total_execution_time = 0
# Some code to evaluate UCS given puzzle
avg_length_solution = total_length_solution/50
avg_length_search = total_length_search/50
avg_nb_nosolution = total_nb_nosolution/50
avg_cost = total_cost/50
avg_execution_time = total_execution_time/50

with open('./output/ucs_analysis.txt', 'w')as f:
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

#Scaling Up

