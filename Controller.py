from Board import Board
from Game import Game
from Graphics import Graphics


class Controller:
    def __init__(self, color: str = 'w') -> None:
        self.game = Game()
        self.graphics = Graphics(self.game.board, color, self)
        self.graphics.start()
        
    def make_move(self, move, promotion=None):
        result = self.game.make_move(move, promotion)
        return result