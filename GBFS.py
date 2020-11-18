import random
import time
from node import Node
from puzzle import Puzzle


def best_first_search(puzzle):
    start = time.time()
    node = Node(puzzle)
    openlist = []
    openlist.append(node)
    closedlist = set()

    while openlist:
        openlist.sort(key=lambda x: x.h_fxn, reverse=True)
        node = openlist.pop()
        if node.state.goal_test():
            print(node)
            print("Solution achieved")
            print(len(closedlist), "paths have been expanded and",
                  len(openlist), "paths remain in the openlist")
            return
        closedlist.add(node)
        for child in node.expand():
            if child not in closedlist and child not in openlist:
                openlist.append(child)
            elif child in openlist:
                if child.f_fxn > node.f_fxn:
                    openlist.remove(child)
                    openlist.append(child)

        now = time.time()
        if (now - start) > 60:
            print('Failed to excecute solution within time restriction')
            return


puzzle1 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle2 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle3 = Puzzle([1, 3, 2, 4, 6, 5, 7, 1], 4, 2)

best_first_search(puzzle1)
print(puzzle2 == puzzle1)
print(puzzle3 == puzzle1)
