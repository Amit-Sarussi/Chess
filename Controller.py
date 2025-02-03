from Board import Board
from Game import Game
from Graphics import Graphics
from Move import Move
from PlayerTypes import PlayerType
from RandomPlayer import RandomPlayer
from Constants import *

class Controller:
    def __init__(self, player1: PlayerType = None, player2: PlayerType = None) -> None:
        self.autoplay = player1 != PlayerType.HumanPlayer
        self.player1 = player1
        self.player2 = player2
        
    def start(self):
        self.game = Game(player1Type=self.player1, player2Type=self.player2)
        if not self.autoplay:
            self.graphics = Graphics(board=self.game.board, color=self.game.turn, controller=self)
            self.graphics.start()
            return {"game_data": self.game.game_data, "result": self.game.checkmate}
        else:
            return self.game.play()
    
    def get_board(self):
        return self.game.board.board_to_FEN()
    
    def get_game_data(self):
        return self.game_data
        
    def make_move(self, move: Move):
        result = self.game.make_move(move)
        return result