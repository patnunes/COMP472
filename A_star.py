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
        openlist.sort(key=lambda x: x.h_fxn, reverse=True)
        node = openlist.pop()
        closedlist.add(node)
        if node.h_fxn == 0:
            print(node)
            print("Solution achieved")
            print(len(closedlist), "paths have been expanded and",
                  len(openlist), "paths remain in the openlist")
            return
<<<<<<< HEAD
        closedlist.add(node)
<<<<<<< HEAD
        for child in node.expand():
=======

        for child in node.expand():
            continue_loop = False
>>>>>>> f5825b2... Modified A* star
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
                if openNode.state == child.state:
                    continue_loop = True
                    break

            if continue_loop:
                continue
=======
        for child in node.expand(puzzle):
            if child not in closedlist and child not in openlist:
                openlist.append(child)
            elif child in openlist:
                if node.less_f_fxn(child):
                    openlist.remove(child)
                    openlist.append(child)
>>>>>>> 5a18425... added heuristics

            openlist.append(child)
        
        now = time.time()
        if (now - start) > 60:
            print('Failed to excecute solution within time restriction')
            return


puzzle1 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle2 = Puzzle([1, 7, 3, 6, 0, 4, 2, 5], 4, 2)
puzzle3 = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 4, 2)

a_star(puzzle2)