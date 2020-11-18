import random
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
        return '{0}(action:{1}, g(node)={2}, h(node)={3}, f(node)={4}, depth={5}, id={6})'.format(
            self.state, self.action, self.g_fxn, self.h_fxn, self.f_fxn, self.depth, self.id
        )

    def expand(self):
        """List all states reachable in one step from current state."""
        children = set()
        action_space = self.state.actions()
        print("LISTACT", action_space)
        for action in action_space:
            children.add(self.child_node(action))

        if(len(action_space) != len(children)):
            print('disaster')

        return children

    def child_node(self, action):
        """Creates the new state based on the action given"""
        next_state = self.state.result(action)
        print('next_state')
        print(next_state)
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