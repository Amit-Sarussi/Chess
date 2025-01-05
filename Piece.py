from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position

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
    def get_legal_moves(self, board):
        pass