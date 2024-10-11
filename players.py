from __future__ import annotations
from abc import abstractmethod
import numpy as np
from random import choice
import tree
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from heuristics import Heuristic
    from board import Board


class PlayerController:
    """Abstract class defining a player
    """
    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        self.player_id = player_id
        self.game_n = game_n
        self.heuristic = heuristic


    def get_eval_count(self) -> int:
        """
        Returns:
            int: The amount of times the heuristic was used to evaluate a board state
        """
        return self.heuristic.eval_count
    

    def __str__(self) -> str:
        """
        Returns:
            str: representation for representing the player on the board
        """
        if self.player_id == 1:
            return 'X'
        return 'O'
        

    @abstractmethod
    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        pass


class MinMaxPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.depth: int = depth


    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """

        # Initialize a tree structure for the current board state
        game_tree = tree.Tree(board.width)
        game_tree.key = board

        # Get the value of the board
        value = self.miniMax(game_tree, self.depth, True)
        best_moves = []

        # Iterate through all the available moves to find the best valued ones and store them in a list
        for col in range(board.width):
            if value == game_tree.children[col].val:
                best_moves.append(col)
        
        # Return a random best move
        return choice(best_moves)
        """
        # Example:
        max_value: float = -np.inf # negative infinity
        max_move: int = 0
        for col in range(board.width):
            if board.is_valid(col):
                new_board: Board = board.get_new_board(col, self.player_id)
                value: int = self.heuristic.evaluate_board(self.player_id, new_board)
                if value > max_value:
                    max_move = col

        # This returns the same as
        self.heuristic.get_best_action(self.player_id, board) # Very useful helper function!

        # This is obviously not enough (this is depth 1)
        # Your assignment is to create a data structure (tree) to store the gameboards such that you can evaluate a higher depths.
        # Then, use the minmax algorithm to search through this tree to find the best move/action to take!

        return max_move
        """
    
    def miniMax(self, game_tree, depth, maximizingPlayer): 
        board = game_tree.key # Get the current board state

        # Check for win
        if self.heuristic.winning(board.get_board_state(), self.game_n) > 0:
            # Return the board value adjusted for depth for quicker wins
            return self.heuristic.evaluate_board(self.player_id, board)-self.game_n+depth
        # If maximum depth has been reached or dra happened evaluate the board
        if depth == 0 or self.heuristic.winning(board.get_board_state(), self.game_n) == -1:
            return self.heuristic.evaluate_board(self.player_id, board)
        
        # Maximizing player tries to get the highest score
        if maximizingPlayer: 
            value = -np.inf # Initialize value to negative infinity
            for col in range(board.width):
                new_node = tree.Tree(board.width) # Create new tree node
                if board.is_valid(col):
                    # Get the new board after making a move in the chosen column
                    new_node.key = board.get_new_board(col, self.player_id)

                    # Calculate the value of the new board recursively
                    new_val = self.miniMax(new_node, depth-1, False)
                    value = max(value, new_val) # Update the maximum value
                    new_node.val = new_val # Store the new value in a node
                # Add the new node to the tree
                game_tree.children[col] = new_node
            return value
        else: # Minimizing player tries to get the lowest score
            value = np.inf # Initialize value to infinity
            for col in range(board.width):
                new_node = tree.Tree(board.width) # Create a new tree node
                if board.is_valid(col):
                    # Get the new board after making a move in the chosen column
                    new_node.key = board.get_new_board(col, self.player_id%2+1)

                    # Calculate the value of the new board
                    new_val = self.miniMax(new_node, depth-1, True)
                    value = min(new_val, value) # Update the minimum value
                    new_node.val = new_val # Store the new value in a node
                # Add the new node to the tree
                game_tree.children[col] = new_node
            return value
                
    

class AlphaBetaPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm with alpha-beta pruning
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.depth: int = depth


    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        # Initialize a tree structure for the current board state
        game_tree = tree.Tree(board.width)
        game_tree.key = board

        # Get the value of the board
        value = self.alphaBeta(game_tree, self.depth, -np.inf, np.inf, True)
        best_moves = []

        # Iterate through all the available moves to find the best valued ones and store them in a list
        for col in range(board.width):
            if value == game_tree.children[col].val:
                best_moves.append(col)
        
        # Return a random best move
        return choice(best_moves)
                
    def alphaBeta(self, game_tree, depth, alpha, beta, maximizingPlayer):
        board = game_tree.key # Get the current board state

        # Check for win
        if self.heuristic.winning(board.get_board_state(), self.game_n) > 0: 
            # Return the board value adjusted for depth for quicker wins
            return self.heuristic.evaluate_board(self.player_id, board)-self.game_n+depth
        # If maximum depth has been reached or draw happened evaluate the board
        if depth == 0 or self.heuristic.winning(board.get_board_state(), self.game_n) == -1:
            return self.heuristic.evaluate_board(self.player_id, board)
        
        # Maximizing player tries to get the highest score 
        if maximizingPlayer:
            value = -np.inf # Initialize value to negative infinity
            for col in range(board.width):
                new_node = tree.Tree(board.width) # Create new tree node
                if board.is_valid(col):
                    # Get the new board after making a move in the chosen column
                    new_node.key = board.get_new_board(col, self.player_id)

                    # Calculate the value of the new board recursively
                    new_val = self.alphaBeta(new_node, depth-1, alpha, beta, False)
                    value = max(value, new_val) # Update the maximum value
                    new_node.val = new_val # Store the new value in a node
                    # Beta cut-off
                    if value > beta:
                        break
                    alpha = max(alpha, value) # Update alpha for further pruning
                # Add the new node to the tree
                game_tree.children[col] = new_node
            return value
        else:  # Minimizing player tries to get the lowest score
            value = np.inf # Initialize the value to infinity
            for col in range(board.width):
                new_node = tree.Tree(board.width) # Create new tree node
                if board.is_valid(col):
                    # Get the new board after making a move in the chosen column
                    new_node.key = board.get_new_board(col, self.player_id%2+1)

                    # Calculate the value of the new board recursively
                    new_val = self.alphaBeta(new_node, depth-1, alpha, beta, True)
                    value = min(value, new_val) # Update the minimum value
                    new_node.val = new_val # Store the new value in a node

                    # Alpha cut-off
                    if value < alpha:
                        break
                    beta = min(beta, value) # Update beta for further pruning
                # Add the new node to the tree
                game_tree.children[col] = new_node
            return value


class HumanPlayer(PlayerController):
    """Class for the human player
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)

    
    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        print(board)

        if self.heuristic is not None:
            print(f'Heuristic {self.heuristic} calculated the best move is:', end=' ')
            print(self.heuristic.get_best_action(self.player_id, board) + 1, end='\n\n')

        col: int = self.ask_input(board)

        print(f'Selected column: {col}')
        return col - 1
    

    def ask_input(self, board: Board) -> int:
        """Gets the input from the user

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        try:
            col: int = int(input(f'Player {self}\nWhich column would you like to play in?\n'))
            assert 0 < col <= board.width
            assert board.is_valid(col - 1)
            return col
        except ValueError: # If the input can't be converted to an integer
            print('Please enter a number that corresponds to a column.', end='\n\n')
            return self.ask_input(board)
        except AssertionError: # If the input matches a full or non-existing column
            print('Please enter a valid column.\nThis column is either full or doesn\'t exist!', end='\n\n')
            return self.ask_input(board)
        