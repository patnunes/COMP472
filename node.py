import numpy as np
import random
from puzzle import Puzzle


class Node:
    """A node. Contains pointer to the parent"""

    def __init__(self, state, parent=None, action=None, heuristic='h1'):
        self.identifier = random.randrange(2147483647)
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.g_fxn = 0  # Distance to start node, cost function
        self.set_h()
        self.set_f()  # Total cost, cost function + heuristic
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        else:
            print(self)

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state and self.g_fxn == other.g_fxn

    def set_g(self, new_g):
        self.g_fxn = new_g

    def set_h(self):
        if self.heuristic == 'h2':
            self.h_fxn = self.h2()
        elif self.heuristic == 'h1':
            self.h_fxn = self.h1()
        else:
            self.h_fxn = self.h0()

    def set_f(self):
        if self.g_fxn == 0:
            g_fxn = 1
        else:
            g_fxn = self.g_fxn

        if self.h_fxn == 0:
            h_fxn = 1
        else:
            h_fxn = self.h_fxn

        self.f_fxn = 2/(1/g_fxn + 1/h_fxn)

    def __repr__(self):

        # solution_path = '{0} {1} {2}'.format(
        #     self.depth, self.g_fxn, self.state
        # )
        search_path = '{0} {1} {2} {3}'.format(
            self.f_fxn, self.g_fxn, self.h_fxn, self.state
        )
        # return solution_path + '\n' + 
        return search_path

    def expand(self):
        """List all states reachable in one step from current state."""
        children = set()
        action_space = self.state.actions()
        for action in action_space:
            children.add(self.child_node(action))

        return children

    def child_node(self, action):
        """Creates the new state based on the action given"""
        next_state = self.state.result(action)
        next_node = Node(next_state, self, action)
        next_node.set_g(self.g_fxn+next_state.get_cost())
        next_node.set_h()
        next_node.set_f()

        return next_node

    def solution_path(self):
        """Return the solution path"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def h0(self) -> int:
        """Zeroth Heuristic; given"""
        if self.state.puzzle[self.state.bot_right] == 0:
            return 0
        return 1

    def h1(self) -> int:
        """First Heuristic; calculates number of miscount from every goal state"""
        goal_1 = 0
        goal_2 = 0
        for i in range(0, self.state.puzzle_size):
            if self.state.goal_state_1[i] != self.state.puzzle[i]:
                goal_1 += 1
            if self.state.goal_state_2[i] != self.state.puzzle[i]:
                goal_2 += 1

        return goal_1

    def h2(self) -> int:
        """Second Heuristic; calculates distance from each goal state"""
        grid1 = self.state.puzzle
        grid2 = self.state.goal_state_1
        grid3 = self.state.goal_state_2
        sub = np.subtract(grid1, grid2)
        diff = np.abs(sub)
        return_val_1 = np.sum(diff.flatten())

        sub = np.subtract(grid1, grid3)
        diff = np.abs(sub)
        return_val_2 = np.sum(diff.flatten())
        return min(return_val_1, return_val_2)
