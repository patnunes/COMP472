import copy
import numpy as np


class Puzzle:

    def __init__(self, puzzle, columns, rows):
        self.puzzle = puzzle
        self.columns = columns
        self.rows = rows
        self.puzzle_size = (len(self.puzzle))
        self.cost = 0
        self.moved_index = 0

        self.top_left = 0
        self.top_right = self.columns - 1
        self.bot_left = self.puzzle_size-self.columns
        self.bot_right = self.puzzle_size-1

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
        for i in range(self.puzzle_size):
            output += str(self.puzzle[i]) + ' '
        return output

    def get_puzzle(self):
        return self.puzzle

    def get_moved_index(self):
        return self.moved_index

    def set_moved_index(self, index):
        self.moved_index = self.puzzle[index]

    def get_cost(self):
        return self.cost

    def find_blank(self):
        return self.puzzle.index(0)

    def goal_test(self):
        current_state = np.array(self.puzzle)
        if np.array_equal(current_state, self.goal_state_1):
            print('Goal state 1 achieved.')
            return True
        if np.array_equal(current_state, self.goal_state_2):
            print('Goal state 2 achieved.')
            return True
        return False

    def swap_positions(self, pos1, pos2):
        current_list = self.puzzle
        current_list[pos1], current_list[pos2] = current_list[pos2], current_list[pos1]
        return current_list

    def move_left(self):
        blank_index = self.find_blank()
        if (blank_index % self.columns == self.columns-1):
            return
        else:
            self.set_moved_index(blank_index+1)
            self.swap_positions(blank_index, blank_index+1)
            self.cost += 1

    def move_right(self):
        blank_index = self.find_blank()
        if (blank_index % self.columns == 0):
            return
        else:
            self.set_moved_index(blank_index-1)
            self.swap_positions(blank_index, blank_index-1)
            self.cost += 1

    def move_up(self):
        blank_index = self.find_blank()
        if (blank_index >= self.puzzle_size - self.columns):
            return
        else:
            self.set_moved_index(blank_index+self.columns)
            self.swap_positions(blank_index, blank_index+self.columns)
            self.cost += 1

    def move_down(self):
        blank_index = self.find_blank()
        if (blank_index < self.columns):
            return
        else:
            self.set_moved_index(blank_index-self.columns)
            self.swap_positions(blank_index, blank_index-self.columns)
            self.cost += 1

    def wrap_right(self):
        blank_index = self.find_blank()
        if (blank_index == self.bot_right):
            self.set_moved_index(self.bot_left)
            self.swap_positions(blank_index, self.bot_left)
            self.cost += 2

        elif (blank_index == self.top_right):
            self.set_moved_index(self.top_left)
            self.swap_positions(blank_index, self.top_left)
            self.cost += 2

    def wrap_left(self):
        blank_index = self.find_blank()
        if (blank_index == self.bot_left):
            self.set_moved_index(self.bot_right)
            self.swap_positions(blank_index, self.bot_right)
            self.cost += 2
        elif (blank_index == self.top_left):
            self.set_moved_index(self.top_right)
            self.swap_positions(blank_index, self.top_right)
            self.cost += 2

    def wrap_down(self):
        
        blank_index = self.find_blank()
        if (blank_index == self.bot_left):
            self.set_moved_index(self.top_left)
            self.swap_positions(blank_index, self.top_left)
            self.cost += 2
        elif (blank_index == self.bot_right):
            self.set_moved_index(self.top_right)
            self.swap_positions(blank_index, self.top_right)
            self.cost += 2

    def wrap_up(self):
        blank_index = self.find_blank()
        if (blank_index == self.top_left):
            self.set_moved_index(self.bot_left)
            self.swap_positions(blank_index, self.bot_left)
            self.cost += 2
        elif (blank_index == self.top_right):
            self.set_moved_index(self.bot_right)
            self.swap_positions(blank_index, self.bot_right)
            self.cost += 2

    def diag_across(self):
        blank_index = self.find_blank()
        if (blank_index == self.top_left):
            self.set_moved_index(self.bot_right)
            self.swap_positions(blank_index, self.bot_right)
            self.cost += 3
            return
        elif (blank_index == self.bot_left):
            self.set_moved_index(self.top_right)
            self.swap_positions(blank_index, self.top_right)
            self.cost += 3
            return
        elif (blank_index == self.top_right):
            self.set_moved_index(self.bot_left)
            self.swap_positions(blank_index, self.bot_left)
            self.cost += 3
            return
        elif (blank_index == self.bot_right):
            self.set_moved_index(self.top_left)
            self.swap_positions(blank_index, self.top_left)
            self.cost += 3
            return

    def diag_adjacent(self):
        blank_index = self.find_blank()
        if (blank_index == self.top_left):
            self.set_moved_index(self.top_left+self.columns+1)
            self.swap_positions(blank_index, self.top_left+self.columns+1)
            self.cost += 3
            return
        elif (blank_index == self.bot_left):
            self.set_moved_index(self.bot_left-self.columns+1)
            self.swap_positions(blank_index, self.bot_left-self.columns+1)
            self.cost += 3
            return
        elif (blank_index == self.top_right):
            self.set_moved_index(self.top_right+self.columns-1)
            self.swap_positions(blank_index, self.top_right+self.columns-1)
            self.cost += 3
            return
        elif (blank_index == self.bot_right):
            self.set_moved_index(self.bot_right-self.columns-1)
            self.swap_positions(blank_index, self.bot_right-self.columns-1)
            self.cost += 3
            return

    def is_corner(self, index):
        if (index == self.top_left or index == self.top_right or index == self.bot_left or index == self.bot_right):
            return True
        else:
            return False

    def actions(self):

        # 'UP', 'DOWN', 'LEFT', 'RIGHT', 'WRAP_LEFT', 'WRAP_RIGHT', 'DIAG_ADJ', 'DIAG_ACROSS'
        possible_actions = []

        blank_index = self.find_blank()
        col_number = blank_index % self.columns

        
        if (self.is_corner(blank_index)):
            if self.rows > 2:
                if blank_index == self.top_left:
                    possible_actions.extend(['WRAP_LEFT', 'DIAG_ADJ', 'DIAG_ACROSS', 'UP', 'LEFT', 'WRAP_UP'])
                elif blank_index == self.top_right:
                    possible_actions.extend(['WRAP_RIGHT', 'DIAG_ADJ', 'DIAG_ACROSS', 'UP', 'RIGHT', 'WRAP_UP'])
                elif blank_index == self.bot_left:
                    possible_actions.extend(['WRAP_LEFT', 'DIAG_ADJ', 'DIAG_ACROSS', 'DOWN', 'LEFT', 'WRAP_DOWN'])
                elif blank_index == self.bot_right:
                    possible_actions.extend(['WRAP_RIGHT', 'DIAG_ADJ', 'DIAG_ACROSS', 'DOWN', 'RIGHT', 'WRAP_DOWN'])
            else:   
                if blank_index == self.top_left:
                    possible_actions.extend(['WRAP_LEFT', 'DIAG_ADJ', 'DIAG_ACROSS', 'UP', 'LEFT'])
                elif blank_index == self.top_right:
                    possible_actions.extend(['WRAP_RIGHT', 'DIAG_ADJ', 'DIAG_ACROSS', 'UP', 'RIGHT'])
                elif blank_index == self.bot_left:
                    possible_actions.extend(['WRAP_LEFT', 'DIAG_ADJ', 'DIAG_ACROSS', 'DOWN', 'LEFT'])
                elif blank_index == self.bot_right:
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
            resulting_state.move_up()
        elif action == 'DOWN':
            resulting_state.move_down()
        elif action == 'LEFT':
            resulting_state.move_left()
        elif action == 'RIGHT':
            resulting_state.move_right()
        elif action == 'WRAP_LEFT':
            resulting_state.wrap_left()
        elif action == 'WRAP_RIGHT':
            resulting_state.wrap_right()
        elif action == 'WRAP_UP':
            resulting_state.wrap_up()
        elif action == 'WRAP_DOWN':
            resulting_state.wrap_down()
        elif action == 'DIAG_ADJ':
            resulting_state.diag_adjacent()
        elif action == 'DIAG_ACROSS':
            resulting_state.diag_across()

        return resulting_state
