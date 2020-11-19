import random
import time
from node import Node
from puzzle import Puzzle


def uniform_cost(puzzle, time_restriction=60, restrict_time=True):
    node = Node(puzzle)
    open_list = []
    open_list.append(node)
    closed_list = []
    start = time.time()

    while open_list:
        open_list.sort(key=lambda x: x.g_fxn, reverse=True)
        node = open_list.pop()
        if node.state.goal_test():
            now = time.time()
            print(node.solution_path())
            print(node.g_fxn)
            print(node)
            print("Solution achieved")
            print(len(closed_list), "paths have been expanded and",
                  len(open_list), "paths remain in the open_list")

            return node, node.g_fxn, closed_list, (now - start)
        closed_list.append(node)

        for child in node.expand():
            continue_loop = False
            for closed_node in closed_list:
                if child.state == closed_node.state:
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
        if ((now - start) > time_restriction) and restrict_time:
            print('Failed to excecute solution within time restriction')
            return node, node.g_fxn, closed_list, (now - start)
