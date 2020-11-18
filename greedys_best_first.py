import random
import time
from node import Node
from puzzle import Puzzle


def best_first_search(puzzle, heuristic='h2'):
    start = time.time()
    node = Node(puzzle, heuristic=heuristic)
    open_list = []
    open_list.append(node)
    closed_list = set()

    while open_list:
        open_list.sort(key=lambda x: x.h_fxn, reverse=True)
        node = open_list.pop()
        closed_list.add(node)
        if node.state.goal_test():
            print(node)
            print("Solution achieved")
            print(len(closed_list), "paths have been expanded and", len(open_list),
                  "paths remain in the open_list.", "node depth", node.depth)
            return

        for child in node.expand():
            continue_loop = False
            print(child)
            print("closed_list size: ", len(closed_list), ", Open list size: ",
                  len(open_list))
            for closed_node in closed_list:
                if child.state == closed_node.state and closed_node.g_fxn < child.g_fxn:
                    continue_loop = True
                    break

            if continue_loop:
                continue

            for open_node in open_list:
                if open_node.state == child.state and child.g_fxn > open_node.g_fxn:
                    continue_loop = True
                    break

            if continue_loop:
                continue

            open_list.append(child)

        now = time.time()
        if (now - start) > 60:
            print('Failed to excecute solution within time restriction')
            return


puzzle1 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle2 = Puzzle([6, 3, 4, 7, 1, 2, 5, 0], 4, 2)
puzzle3 = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 4, 2)

best_first_search(puzzle3)
