from abc import ABC, abstractmethod
import math
import random
import numpy as np
import time
import math
import copy

"""Implementation of all Player Agents."""

class Player(ABC):
    """Abstract class to represent all types of Players."""

    @abstractmethod
    def play(self, board):
        """
        Return the column to play in given the state of the board.
        Must be implemented by subclasses
        """
        pass

class RandomPlayer(Player):
    """Player who selects a valid move at random."""
    def play(self, board):
        return np.random.choice(board.valid_moves())


class Node:
    def __init__(self, board, parent=None): # does state need to capture board and player here ...
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.board = board 

    
    def expand(self):
        if self.board.winner is None: # game has not ended
            for move in self.board.valid_moves():
                # get a new board state that results from apply this move
                new_board = copy.deepcopy(self.board)
                new_board.make_move(move)
                child_node = Node(new_board, self)
                self.children.append(child_node)
            return True
        return False

    def select_best_child(self, c):
        """return the child with the highest upper confidence bound."""
        scores = [child.ucb_score(c) for child in self.children]
        indx = np.argmax(scores)
        return self.children[indx]

    def best_move(self):
        scores = [child.visits for child in self.children]
        indx = np.argmax(scores)
        return self.board.valid_moves()[indx]

    def rollout(self):
        """play randomly from the current state until game terminates"""
        board = copy.deepcopy(self.board)
        
        while board.winner is None:
            valid_moves = board.valid_moves()
            move = np.random.choice(valid_moves)
            board.make_move(move)
        return board.winner

    def back_propagate(self, outcome):
        self.visits +=1
        if outcome == 'TIE':
            self.wins += 0.5
        elif outcome == self.board.current_player:
            self.wins +=1
        if self.parent:
            self.parent.back_propagate(outcome)
        
    def ucb_score(self, c=2):
        if self.visits == 0:
            return np.inf
        mu = self.wins/self.visits
        parent = self.parent if self.parent else self
        return mu + c*math.sqrt(math.log(parent.visits)/self.visits)
    
    def is_leaf(self): # will always be true initially
        return len(self.children)==0

    


class MCTSPlayer:
    """Monte Carlo Tree Search player"""

    def __init__(self, c=1.4, max_time=5):
        self.c = c # parameter for UCB
        self.max_time=max_time
        #self.max_iter = max_iter # maximum number of seconds to explore before selecting move

    def play(self, board):

        start = time.time()

        current_node = Node(board)
        #for _ in range(self.max_iter):
        iter = 0
        while time.time() - start < self.max_time:
            self.search_board(current_node)
            iter +=1
            
        print(f'selected move in {iter} iterations')
        return current_node.best_move()
        
    def search_board(self, node):

        # selection - move down the tree
        while not node.is_leaf():
            node = node.select_best_child(self.c)

        # expansion phase
        if node.expand():
            node = node.select_best_child(self.c)

            # rollout phase
            outcome = node.rollout()

            # backprop phase
            node.back_propagate(outcome)     
        else:
            node.back_propagate(node.board.winner)   


    
class HumanPlayer(Player):
    """Human player - asks for moves via standard input."""
    
    def play(self, board):
        valid_moves = board.valid_moves()
        move = self.int_input('What column would you like to play in (columns are zero indexed):')
        while move not in valid_moves:
            move = self.int_input(f'Sorry, {move} is invalid. Please choose one of {valid_moves}')
        return move

    @staticmethod
    def int_input(message):
        """
        function that tries to convert input to an int
        """
        try: 
            value = int(input(message))
            return value
        except ValueError:
            return message