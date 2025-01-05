from Board import Board
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, board: Board, color: str = 'w') -> None:
        self.color = color
        self.board = board
    
    @abstractmethod
    def get_player_move(self):
        pass
