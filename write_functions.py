from node import Node
from uniform_cost import uniform_cost
from greedys_best_first import best_first_search
from A_star import a_star
from puzzle import Puzzle

def write_solution(ctr,output_directory, execution_time, goal_node, total_cost, algo, heuristic=None):
        if heuristic is None:
            file_name = '%s_%s_solution.txt' % (ctr, algo)
        else:
            file_name = '%s_%s-%s_solution.txt' % (ctr, algo, heuristic)


        if execution_time >= 60:
            with open(output_directory + '/' + file_name, 'w') as file:
                file.write('No solution')
        else:
            solution_path = goal_node.solution_path()
            output_lines = []
            for node in solution_path:
                output_lines.append(str(node.state).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip())
            output_lines.append('%d %f' % (total_cost, execution_time))
            with open(output_directory + '/' + file_name, 'w') as file:
                file.writelines("%s\n" % i for i in output_lines)
        file.close()



def write_search(ctr,output_directory, execution_time,  closed_list,  algo, heuristic=None):
    print(closed_list)
    if heuristic is None:
            file_name = '%s_%s_search.txt' % (ctr, algo)
    else:
            file_name = '%s_%s-%s_search.txt' % (ctr, algo, heuristic)
    
    if execution_time > 60:
            with open(output_directory + '/' + file_name, 'w') as file:
                file.write('No solution')

    else:
        # output_lines = []
        file = open(output_directory + '/' + file_name, 'w')
        # for node in closed_list:
        #     output_lines.append(str(node.state).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').replace(',','\n').strip())
           
        with open(output_directory + '/' + file_name, 'w') as file:
            file.writelines("%s\n" % i for i in closed_list) 
    file.close()

def write_analysis(output_directory, fifty_puzzle_file, algo, cols, rows, puzzle_qty, heuristic=None ):

    if heuristic is None:
            file_name = '%s_analysis.txt' % (algo)
    else:
            file_name = '%s-%s_analysis.txt' % (algo, heuristic)

    total_length_solution =0
    total_length_search = 0
    total_nb_nosolution = 0
    total_cost_50 = 0
    total_execution_time = 0
    
    with open(fifty_puzzle_file) as file:
        for line in file:
            temp_puzzle = list(map(int ,line.split(' ')))
            puzzle = Puzzle(temp_puzzle, cols, rows)

            if algo == 'ucs':
                goal_node, total_cost, closedlist, execution_time = uniform_cost(puzzle)
            elif algo == 'gbfs':
                goal_node, total_cost, closedlist, execution_time = best_first_search(puzzle, heuristic= heuristic)
            elif algo == 'astar':
                goal_node, total_cost, closedlist, execution_time = a_star(puzzle, heuristic=heuristic)

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

    with open(output_directory + '/' + file_name, 'w') as f:
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