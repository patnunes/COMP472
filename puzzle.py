import numpy as np
import copy


class Puzzle:

    def __init__(self, puzzle, columns, rows):
        self.puzzle = puzzle
        self.columns = columns
        self.rows = rows
        self.puzzle_size = (len(self.puzzle))
        self.cost = 0

        self.topLeft = 0
        self.topRight = self.columns - 1
        self.botLeft = self.puzzle_size-self.columns
        self.botRight = self.puzzle_size-1

        core_indices = (np.arange(self.columns*self.rows) + 1) % (self.columns*self.rows)
        self.goal_state_1 = core_indices
        self.goal_state_2 = core_indices.reshape(self.rows, self.columns, order='F').reshape(
            1, self.rows*self.columns)[0]

    def __eq__(self, other):
        for i in range(self.puzzle_size):
            if (self.puzzle[i] != other.puzzle[i]):
                return False
        return True

    def __repr__(self):
        output = ''
        for i in range(self.rows):
            output += str(self.puzzle[i*self.columns:(i+1)*self.columns])+'\n'
        return output

    def get_puzzle(self):
        return self.puzzle

    def get_cost(self):
        return self.cost

    def find_blank(self):
        return self.puzzle.index(0)

    def goal_test(self):
        current_state = np.array(self.puzzle)
        if np.array_equal(current_state, self.goal_state_1) or np.array_equal(current_state, self.goal_state_2):
            return True
        return False

    def swapPositions(self, pos1, pos2):
        current_list = self.puzzle
        current_list[pos1], current_list[pos2] = current_list[pos2], current_list[pos1]
        return current_list

    def moveLeft(self):
        blank_index = self.find_blank()
        if (blank_index % self.columns == self.columns-1):
            return
        else:
            self.swapPositions(blank_index, blank_index+1)
            self.cost += 1

    def moveRight(self):
        blank_index = self.find_blank()
        if (blank_index % self.columns == 0):
            return
        else:
            self.swapPositions(blank_index, blank_index-1)
            self.cost += 1

    def moveUp(self):
        blank_index = self.find_blank()
        if (blank_index >= self.puzzle_size - self.columns):
            return
        else:
            self.swapPositions(blank_index, blank_index+self.columns)
            self.cost += 1

    def moveDown(self):
        blank_index = self.find_blank()
        if (blank_index < self.columns):
            return
        else:
            self.swapPositions(blank_index, blank_index-self.columns)
            self.cost += 1

    def wrapRight(self):
        blank_index = self.find_blank()
        if (blank_index == self.botRight):
            self.swapPositions(blank_index, self.botLeft)
            self.cost += 2

        elif (blank_index == self.topRight):
            self.swapPositions(blank_index, self.topLeft)
            self.cost += 2

    def wrapLeft(self):
        blank_index = self.find_blank()
        if (blank_index == self.botLeft):
            self.swapPositions(blank_index, self.botRight)
            self.cost += 2
        elif (blank_index == self.topLeft):
            self.swapPositions(blank_index, self.topRight)
            self.cost += 2

    def diagAcross(self):
        blank_index = self.find_blank()
        if (blank_index == self.topLeft):
            self.swapPositions(blank_index, self.botRight)
            self.cost += 3
            return
        elif (blank_index == self.botLeft):
            self.swapPositions(blank_index, self.topRight)
            self.cost += 3
            return
        elif (blank_index == self.topRight):
            self.swapPositions(blank_index, self.botLeft)
            self.cost += 3
            return
        elif (blank_index == self.botRight):
            self.swapPositions(blank_index, self.topLeft)
            self.cost += 3
            return

    def diagAdjacent(self):
        blank_index = self.find_blank()
        if (blank_index == self.topLeft):
            self.swapPositions(blank_index, self.topLeft+self.columns+1)
            self.cost += 3
            return
        elif (blank_index == self.botLeft):
            self.swapPositions(blank_index, self.botLeft-self.columns+1)
            self.cost += 3
            return
        elif (blank_index == self.topRight):
            self.swapPositions(blank_index, self.topRight+self.columns-1)
            self.cost += 3
            return
        elif (blank_index == self.botRight):
            self.swapPositions(blank_index, self.botRight-self.columns-1)
            self.cost += 3
            return

    def isCorner(self, index):
        if (index == self.topLeft or index == self.topRight or index == self.botLeft or index == self.botRight):
            return True
        else:
            return False

    def actions(self):

        # 'UP', 'DOWN', 'LEFT', 'RIGHT', 'WRAP_LEFT', 'WRAP_RIGHT', 'DIAG_ADJ', 'DIAG_ACROSS'
        possible_actions = []

        blank_index = self.find_blank()
        col_number = blank_index % self.columns
        if (self.isCorner(blank_index)):
            if blank_index == self.topLeft:
                possible_actions.extend(['WRAP_LEFT', 'DIAG_ADJ', 'DIAG_ACROSS', 'UP', 'LEFT'])
            elif blank_index == self.topRight:
                possible_actions.extend(['WRAP_RIGHT', 'DIAG_ADJ', 'DIAG_ACROSS', 'UP', 'RIGHT'])
            elif blank_index == self.botLeft:
                possible_actions.extend(['WRAP_LEFT', 'DIAG_ADJ', 'DIAG_ACROSS', 'DOWN', 'LEFT'])
            elif blank_index == self.botRight:
                possible_actions.extend(['WRAP_RIGHT', 'DIAG_ADJ', 'DIAG_ACROSS', 'DOWN', 'RIGHT'])
        else:
            if col_number == 0:
                possible_actions.extend(['UP', 'DOWN', 'LEFT'])
            elif col_number == self.columns-1:
                possible_actions.extend(['UP', 'DOWN', 'RIGHT'])
            elif blank_index >= self.puzzle_size - self.columns:
                possible_actions.extend(['DOWN', 'RIGHT', 'LEFT'])
            elif blank_index < self.columns:
                possible_actions.extend(['UP', 'RIGHT', 'LEFT'])
            else:
                possible_actions.extend(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        return possible_actions

    def result(self, action):
        resulting_state = copy.deepcopy(self)
        if action == 'UP':
            resulting_state.moveUp()
        elif action == 'DOWN':
            resulting_state.moveDown()
        elif action == 'LEFT':
            resulting_state.moveLeft()
        elif action == 'RIGHT':
            resulting_state.moveRight()
        elif action == 'WRAP_LEFT':
            resulting_state.wrapLeft()
        elif action == 'WRAP_RIGHT':
            resulting_state.wrapRight()
        elif action == 'DIAG_ADJ':
            resulting_state.diagAdjacent()
        elif action == 'DIAG_ACROSS':
            resulting_state.diagAcross()
        return resulting_state

    def h0(self):
        if self.get_puzzle()[-1] == 0:
            return 0
        else:
            return 1
