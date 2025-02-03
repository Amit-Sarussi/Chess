from abc import ABC, abstractmethod

from Move import Move

class Piece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.char = ''

    def __str__(self):
        return f'{self.color} {self.__class__.__name__} at {self.position}'

    def __repr__(self):
        return self.__str__()

    def set_position(self, new_pos):
        self.position = new_pos
    
    @abstractmethod
    def piece_to_filename(self):
        pass

    @abstractmethod
    def get_pseudo_legal_moves(self, board, special_moves=True):
        """
        Generate all pseudo-legal moves for the piece on the given board.
        Pseudo-legal moves are moves that the piece can make according to its movement rules,
        without considering whether the move would leave the king in check.
        Args:
            board (Board): The current state of the chess board.
        Returns:
            list: A list of pseudo-legal moves available for the piece.
        """
        
        pass

    def get_char(self):
        return self.char.upper() if self.color == 'w' else self.char
    
    def convert_move(self, start, a_move):
        if len(a_move) == 3:
            return Move(start, (a_move[0], a_move[1]), a_move[2])
        else:
            return Move(start, (a_move[0], a_move[1]))