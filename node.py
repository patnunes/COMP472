
import time
from puzzle import Puzzle
class Node:
    """A node. Contains pointer to the parent"""

    def __init__(self, state, parent=None, action=None, g_fxn=0):
        self.state = state
        self.parent = parent
        self.g_fxn = 0  # Distance to start node, cost function
        self.h_fxn = 0  # Distance to goal node, heuristic
        self.f_fxn = 0  # Total cost, cost function + heuristic
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return '{0}(action:{1}, g(node)={2}, h(node)={3}, f(node)={4})'.format(self.state, self.action, self.g_fxn, self.h_fxn, self.f_fxn)
    
    def less_h_fxn(self, other):
        """compares h_fxn value for 2 nodes"""
        return self.h_fxn < other.h_fxn
    
    def less_g_fxn(self, other):
        """compares g_fxn value for 2 nodes"""
        return self.g_fxn < other.g_fxn
    
    def __lt__(self, other):
        """For use with A*, compares f_fxn between two nodes"""
        return self.f_fxn < other.f_fxn

    def expand(self, puzzle):
        """List all states reachable in one step from current state."""
        return [self.child_node(puzzle, action)
                for action in puzzle.actions(self.state)]

    def child_node(self, puzzle, action):
        next_state = puzzle.result(self.state, action)
        next_node = Node(next_state, self, action, puzzle.g_fxn(self.g_fxn, self.state, action, next_state))
        return next_node

    def solution_path(self):
        """Return the solution path"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

def uniform_cost(puzzle):
    start = time.time()
    node = Node(puzzle())
    openlist = []
    openlist.append(node)
    closedlist = []

    while openlist:
        node = openlist.pop()
        if puzzle.goal_test(node.state):
            print(len(closedlist), "paths have been expanded and", len(openlist), "paths remain in the openlist")
            return
        closedlist.append(node.state)
        for child in node.expand(puzzle):
            print(child)
            if child.state not in closedlist and child not in openlist:
                 openlist.append(child)
            elif child in openlist:
                if node.less_g_fxn(child):
                    del openlist[child]
                    openlist.append(child)
                    openlist.sort(node.g_fxn)
            
        now = time.time()
        if (now - start) > 60:
            return


puzzle1 = Puzzle([3, 0, 1, 4, 2, 6, 5, 7], 2,4)

uniform_cost(puzzle1)