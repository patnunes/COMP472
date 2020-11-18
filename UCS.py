import random
import time
from node import Node
from puzzle import Puzzle


def uniform_cost(puzzle):
    node = Node(puzzle)
    openlist = []
    openlist.append(node)
    closedlist = []
    visited_nodes = 0

    while openlist:
        openlist.sort(key=lambda x: x.g_fxn, reverse=True)
        node = openlist.pop()
        if node.state.goal_test():
            print(node.solution_path())
            print(node.g_fxn)
            print(node)
            print("Solution achieved")
            print(len(closedlist), "paths have been expanded and",
                  len(openlist), "paths remain in the openlist")
            return node, node.g_fxn
        closedlist.append(node)
        for child in node.expand():
            visited_nodes += 1
            if child not in closedlist and child not in openlist:
                openlist.append(child)
            elif child in openlist:
                if child.g_fxn > node.g_fxn:
                    openlist.remove(child)
                    openlist.append(child)