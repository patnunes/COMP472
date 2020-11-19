from node import Node

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