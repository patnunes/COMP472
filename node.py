import numpy as np
import random
from puzzle import Puzzle


class Node:
    """A node. Contains pointer to the parent"""

    def __init__(self, state, parent=None, action=None, heuristic='h1'):
        self.id = random.randrange(2147483647)
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.g_fxn = 0  # Distance to start node, cost function
        self.set_h()
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
        if self.heuristic == 'h2':
            self.h_fxn = self.h2()
        elif self.heuristic == 'h1':
            self.h_fxn = self.h1()
        else:
            self.h_fxn = self.h0()

    def set_f(self):
        self.f_fxn = self.g_fxn + self.h_fxn

    def __repr__(self):
        return '{0}(action:{1}, g(node)={2}, h(node)={3}, f(node)={4}, depth={5}, id={6})'.format(
            self.state, self.action, self.g_fxn, self.h_fxn, self.f_fxn, self.depth, self.id
        )

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
        if self.state.goal_test() is True:
            return 1
        return 0

    def h1(self) -> int:
        goal_1 = 0
        goal_2 = 0
        for i in range(0, self.state.puzzle_size):
            if self.state.goal_state_1[i] != self.state.puzzle[i]:
                goal_1 += 1
            if self.state.goal_state_2[i] != self.state.puzzle[i]:
                goal_2 += 1

        return max(goal_1, goal_2)

    def h2(self) -> int:
        grid1 = self.state.puzzle
        grid2 = self.state.goal_state_1
        grid3 = self.state.goal_state_2
        sub = np.subtract(grid1, grid2)
        diff = np.abs(sub)
        return_val_1 = np.sum(diff.flatten())

        sub = np.subtract(grid1, grid3)
        diff = np.abs(sub)
        return_val_2 = np.sum(diff.flatten())
        return max(return_val_1, return_val_2)
