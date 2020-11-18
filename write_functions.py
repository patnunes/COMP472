from node import Node

def write_solution(output_directory, execution_time, goal_node, total_cost, algo, heuristic=None):
        if heuristic is None:
            file_name = '0_%s_solution.txt' % (algo)
        else:
            file_name = '0_%s-%s_solution.txt' % (algo, heuristic)


        if execution_time > 60:
            with open(output_directory + '/' + file_name, 'w') as file:
                file.write('No solution')
        else:
            solution_path = goal_node.solution_path()
            output_lines = []
            for node in solution_path:
                #configuration = str(node.configuration).replace('[', '').replace(']', '').replace(',', '').strip()
                output_lines.append(str(node.state).replace('[', '').replace(']', '').replace(',', '').replace('\n',' ').strip())
            output_lines.append('%d %f' % (total_cost, execution_time))
            with open(output_directory + '/' + file_name, 'w') as file:
                file.writelines(str(output_lines))

def write_search_path(output_directory, execution_time, solution_path, algo):
    return