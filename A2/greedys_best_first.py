import random
import time
from node import Node
from puzzle import Puzzle


def best_first_search(puzzle, heuristic='h1', time_restriction=60, restrict_time=True):
    start = time.time()
    node = Node(puzzle, heuristic=heuristic)
    open_list = []
    open_list.append(node)
    closed_list = set()

    while open_list:
        open_list.sort(key=lambda x: x.h_fxn, reverse=True)
        node = open_list.pop()
        closed_list.add(node)
        print(node)
        if node.state.goal_test():
            now = time.time()
            print(node)
            print("Solution achieved")
            print(len(closed_list), "paths have been expanded and", len(open_list),
                  "paths remain in the open_list.", "node depth", node.depth)

            return node, node.g_fxn, closed_list, (now - start)

        for child in node.expand():
            add_node = True
            for closed_node in closed_list:
                if child.state == closed_node.state:
                    add_node = False
                    break
            if add_node:
                open_list.append(child)

        now = time.time()
        if ((now - start) > time_restriction) and restrict_time:
            print('Failed to excecute solution within time restriction')
            return node, node.g_fxn, closed_list, (now - start)
