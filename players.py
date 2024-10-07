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

        # TODO: implement minmax algortihm!
        # INT: use the functions on the 'board' object to produce a new board given a specific move
        # HINT: use the functions on the 'heuristic' object to produce evaluations for the different board states!

        
        game_tree = tree.Tree(board.width)
        game_tree.key = board
        value  = self.miniMax(game_tree, self.depth, True)
        best_moves = []
        for col in range(board.width):
            if game_tree.children[col].val == value:
                best_moves.append(col)
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
        board = game_tree.key
        if depth == 0 or self.heuristic.winning(board.get_board_state(), self.game_n):
            return self.heuristic.evaluate_board(self.player_id, board)
        if maximizingPlayer:
            max_value = -np.inf
            for col in range(board.width):
                new_node = tree.Tree(board.width)
                if board.is_valid(col):
                    new_node.key = board.get_new_board(col, self.player_id)
                    value = self.miniMax(new_node, depth-1, False)
                    new_node.val = value
                    max_value = max(max_value, value)
                game_tree.children[col] = new_node
            return max_value
        else:
            min_value = np.inf
            for col in range(board.width):
                new_node = tree.Tree(board.width)
                if board.is_valid(col):
                    new_node.key = board.get_new_board(col, switchPlayer(self.player_id))
                    value= self.miniMax(new_node, depth-1, True)
                    new_node.val = value
                    min_value = min(min_value, value)
                game_tree.children[col] = new_node
            return min_value
                
    

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
        game_tree = tree.Tree(board.width)
        game_tree.key = board
        value = self.alphaBeta(game_tree, self.depth, -np.inf, np.inf, True)
        best_move = []
        for col in range(board.width):
            if value+1 == game_tree.children[col].val:
                best_move.append(col)
        return choice(best_move)
                
    def alphaBeta(self, game_tree, depth, alpha, beta, maximizingPlayer):
        board = game_tree.key
        if depth == 0 or self.heuristic.winning(board.get_board_state(), self.game_n) != 0:
            return self.heuristic.evaluate_board(self.player_id, board)
        if maximizingPlayer:
            value = -np.inf
            for col in range(board.width):
                new_node = tree.Tree(board.width)
                if board.is_valid(col):
                    new_board = board.get_new_board(col, self.player_id)
                    new_node.key = new_board
                    new_val = self.alphaBeta(new_node, depth-1, alpha, beta, False)
                    value = max(value, new_val)
                    new_node.val = new_val
                    if value > beta:
                        break
                    alpha = max(alpha, value)
                game_tree.children[col] = new_node
            return value-1
        else:
            value = np.inf
            for col in range(board.width):
                new_node = tree.Tree(board.width)
                if board.is_valid(col):
                    new_board = board.get_new_board(col, switchPlayer(self.player_id))
                    new_node.key = new_board
                    game_tree.children[col] = new_node
                    new_val = self.alphaBeta(new_node, depth-1, alpha, beta, True)
                    value = min(value, new_val)
                    new_node.val = new_val
                    if value < alpha:
                        break
                    beta = min(beta, value)
                game_tree.children[col] = new_node
            return value-1

def switchPlayer(player_id):
    if player_id == 1:
        return 2
    else:
        return 1


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
        