import json
from Board import Board
from Constants import *
from Graphics import Graphics
from Move import Move

class GameViewer:
    def __init__(self, filename, time_between=1000):
        self.filename = filename
        self.time_between = time_between
        data = self.get_data_from_gamefile()
        self.moves = data["data"]
        self.starting_fen = data["starting_fen"]
        if data["result"] == 'w':
            self.checkmate = 'b';
        elif data["result"] == 'b':
            self.checkmate = 'w';
        else:
            self.checkmate = 't'
        self.board = Board(FEN_board=self.starting_fen, color='w')
        self.graphics = Graphics(self.board, 'w', spectate_mode=True, GameViewer=self)
        self.graphics.start()
    
    def make_next_move(self):
        if len(self.moves) == 0: return None
        notation_move = self.moves[0]
        move: Move = Move.notation_to_move(notation_move)
        self.board.make_move(move)
        self.moves = self.moves[1:]
        return move


    def get_data_from_gamefile(self):
        with open(GAME_DATA_DIR + self.filename + ".json", 'r') as f:
            data = json.load(f)
            return data
