import random
import time
from scipy.spatial.distance import cdist

from puzzle import Puzzle


class Node:
    """A node. Contains pointer to the parent"""

    def __init__(self, state, parent=None, action=None, heuristic=''):
        self.id = random.randrange(2147483647)
        self.state = state
        self.parent = parent
        self.g_fxn = 0  # Distance to start node, cost function
        self.h_fxn = 0  # Distance to goal node, heuristic
        self.f_fxn = 0  # Total cost, cost function + heuristic
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def set_g(self, new_g):
        self.g_fxn = new_g

    def set_h(self):
        temp = 0
        for i in range(0, self.state.puzzle_size):
            if self.state.goal_state_1[i] != self.state.puzzle[i]:
                temp += 1
        self.h_fxn = temp

    def set_f(self):
        self.f_fxn = self.g_fxn + self.h_fxn

    def __repr__(self):
        return '{0}(action:{1}, g(node)={2}, h(node)={3}, f(node)={4}, depth={5}, id={6}, parent_id={7})'.format(
            self.state, self.action, self.g_fxn, self.h_fxn, self.f_fxn, self.depth, self.id, self.parent.id
        )

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
        listR = [self.child_node(puzzle, action)
                 for action in puzzle.actions(self.state)]
        listActions = []
        for action in puzzle.actions(self.state):
            listActions.append(action)
        print("LISTACT", listActions)
        return listR

    def child_node(self, puzzle, action):
        """Creates the new state based on the action given"""
        next_state = puzzle.result(action)
        next_node = Node(next_state, self, action)
        next_node.set_g(self.g_fxn+next_state.get_cost())
        next_node.set_f()
        next_node.set_h()
        return next_node

    def solution_path(self):
        """Return the solution path"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def best_first_search(puzzle):
    start = time.time()
    node = Node(puzzle)
    openlist = []
    openlist.append(node)
    closedlist = set()

    while openlist:
        openlist.sort(key=lambda x: x.h_fxn)
        node = openlist.pop()
        if node.state.goal_test():
            print(node)
            print("Solution achieved")
            print(len(closedlist), "paths have been expanded and",
                  len(openlist), "paths remain in the openlist")
            return
        closedlist.add(node)
        for child in node.expand(puzzle):
            print(child)
            print("Closedlist size: ", len(closedlist), ", Open list size: ",
                  len(openlist))
            if child not in closedlist and child not in openlist:
                openlist.append(child)
            # elif child in openlist:
            #     if node.less_f_fxn(child):
            #         openlist.remove(child)
            #         openlist.append(node)

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
