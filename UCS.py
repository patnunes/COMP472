import random
import time
from node import Node
from puzzle import Puzzle


def uniform_cost(puzzle):
    start = time.time()
    node = Node(puzzle)
    openlist = []
    openlist.append(node)
    closedlist = []
    visited_nodes = 0

    while openlist:
        openlist.sort(key=lambda x: x.g_fxn, reverse=True)
        node = openlist.pop()
        if node.state.goal_test():
            print(node)
            print("Solution achieved")
            print(len(closedlist), "paths have been expanded and",
                  len(openlist), "paths remain in the openlist")
            return
        closedlist.append(node)
        for child in node.expand():
            visited_nodes += 1
            if child not in closedlist and child not in openlist:
                openlist.append(child)
            elif child in openlist:
                if child.g_fxn > node.g_fxn:
                    openlist.remove(child)
                    openlist.append(child)

        now = time.time()
        if (now - start) > 60:
            print('Failed to excecute solution within time restriction')
            return


puzzle1 = Puzzle([1, 2, 0, 3, 5, 6, 7, 4], 4, 2)
puzzle2 = Puzzle([6, 3, 4, 7, 1, 2, 5, 0], 4, 2)
puzzle3 = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 4, 2)

uniform_cost(puzzle3)
# print(puzzle2 == puzzle1)
# print(puzzle3 == puzzle1)
