import random
import time
from node import Node
from puzzle import Puzzle


def a_star(puzzle):
    start = time.time()
    node = Node(puzzle)
    openlist = []
    openlist.append(node)
    closedlist = set()

    while openlist:

        print("OPEN SIZE: ")
        print(len(openlist))
        print("\n")
        openlist.sort(key=lambda x: x.f_fxn, reverse=True)
        node = openlist.pop()
        closedlist.add(node)
        if node.h_fxn == 0:
            print(node)
            print("node depth", node.depth)
            print("Solution achieved")
            print(len(closedlist), "paths have been expanded and",
                  len(openlist), "paths remain in the openlist")
            return

        for child in node.expand():
            continue_loop = False
            print(child)
            print("Closedlist size: ", len(closedlist), ", Open list size: ",
                  len(openlist))
            for closedNode in closedlist:
                if child.state == closedNode.state and closedNode.g_fxn < child.g_fxn:
                    continue_loop = True
                    break

            if continue_loop:
                continue

            for openNode in openlist:
                if openNode.state == child.state and child.g_fxn > openNode.g_fxn:
                    continue_loop = True
                    break

            if continue_loop:
                continue

            openlist.append(child)
        
        now = time.time()
        if (now - start) > 60:
            print('Failed to excecute solution within time restriction')
            return

puzzle1 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle2 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle3 = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 4, 2)

a_star(puzzle1)