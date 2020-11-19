import time
from node import Node
from puzzle import Puzzle


def a_star(puzzle, heuristic='h2', time_restriction=60):
    start = time.time()
    node = Node(puzzle, heuristic=heuristic)
    open_list = []
    open_list.append(node)
    closed_list = set()

    while open_list:
        open_list.sort(key=lambda x: x.f_fxn, reverse=True)
        node = open_list.pop()
        closed_list.add(node)
        print(node)
        if node.state.goal_test():
            now = time.time()
            print("Solution achieved")
            print(len(closed_list), "paths have been expanded and", len(open_list),
                  "paths remain in the open_list.", "node depth", node.depth)
            return node, node.g_fxn, closed_list, (now - start)

        for child in node.expand():
            continue_loop = False
            for closed_node in closed_list:
                if child.state == closed_node.state and closed_node.f_fxn < child.f_fxn:
                    continue_loop = True
                    break

            if continue_loop:
                continue

            for open_node in open_list:
                if open_node.state == child.state and child.f_fxn > open_node.f_fxn:
                    continue_loop = True
                    break

            if continue_loop:
                continue

            open_list.append(child)

        now = time.time()
        if (now - start) > time_restriction:
            print('Failed to excecute solution within time restriction')
            return node, node.g_fxn, closed_list, (now - start)


puzzle1 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle2 = Puzzle([6, 3, 4, 7, 1, 2, 5, 0], 4, 2)
puzzle3 = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 4, 2)

a_star(puzzle2)
