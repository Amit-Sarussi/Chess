from Board import Board
from Game import Game
from Graphics import Graphics
from Move import Move
from PlayerTypes import PlayerType
from RandomPlayer import RandomPlayer
class Controller:
    def __init__(self, player1: PlayerType, player2: PlayerType) -> None:
        if player1 == PlayerType.HumanPlayer:
            self.graphics = Graphics(self.game.board, "w", self)
            
        if player2 == PlayerType.RandomPlayer:
            self.player2 = RandomPlayer(self.game.board, "b")


        self.game = Game(player1)
        self.graphics.start()
        
    def make_move(self, move: Move):
        result = self.game.make_move(move)
        return result