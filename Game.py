from Board import Board
from Constants import *
from PlayerTypes import PlayerType
from RandomPlayer import RandomPlayer
from King import King
from Rook import Rook
from Move import Move

class Game:
    def __init__(self, player1Type: PlayerType=None, player2Type: PlayerType=None):
        self.board: Board = Board(FEN_board=STARTING_FEN, color='w')
        self.turn = self.board.turn # 'w' or 'b'
        self.game_data = {"starting_fen": STARTING_FEN, "data": []}

        match player1Type:
            case PlayerType.RandomPlayer:
                self.player1 = RandomPlayer(self.board, color='w')
            case PlayerType.HumanPlayer:
                self.player1 = None
            case _:
                self.player1 = None
                print("ERROR IN PLAYER'S TYPE CHOICE")

        match player2Type:
            case PlayerType.RandomPlayer:
                self.player2 = RandomPlayer(self.board, color='b')
            case PlayerType.HumanPlayer:
                self.player2 = None
                print("ERROR IN PLAYER'S TYPE CHOICE")
            case _:
                self.player2 = None
                print("ERROR IN PLAYER'S TYPE CHOICE")
        

        self.checkmate = None

    def make_move(self, move: Move):
        # Validate move
        if self.board.validate_move(move, color=self.turn, check_pseudo_legal=True, log=True) == False:
            return False, None, None
        
        self.game_data["data"].append(move.move_to_notation())
        
        
        self.board.make_move(move)
        
        self.turn = 'w' if self.turn == 'b' else 'b'

        # Check if random player is in checkmate
        if len(self.board.get_all_valid_moves(self.turn)) == 0:
            # Check if king in check
            if self.board.is_king_in_check(self.turn):
                self.checkmate = "w" if self.turn == "b" else self.turn
            else:
                self.checkmate = "t"
            self.game_data["result"] = self.checkmate if self.checkmate in ('w', 'b') else 't'    
            return True, move, self.checkmate

        # make random player move:
        move = self.player2.get_player_move()
        self.game_data["data"].append(move.move_to_notation())
        
        self.board.make_move(move)
        self.turn = 'w' if self.turn == 'b' else 'b'
        
        # Check if player has available moves
        if len(self.board.get_all_pseudo_legal_moves(self.turn)) == 0:
            if self.board.is_king_in_check(self.turn):
                self.checkmate = "w" if self.turn == "b" else self.turn
            else:
                self.checkmate = "t"
            self.game_data["result"] = self.checkmate if self.checkmate in ('w', 'b') else 't' 

        return True, move, self.checkmate

    def play(self):
        while self.checkmate == None and self.board.halfmove <= 50:
            # Get move
            if self.turn == "w":
                move = self.player1.get_player_move()
            else:
                move = self.player2.get_player_move()

            if move == None:
                if self.board.is_king_in_check(self.turn):
                    self.checkmate = "w" if self.turn == "b" else self.turn
                else:
                    self.checkmate = "t"
                break
            
            self.game_data["data"].append(move.move_to_notation())
            
            # Submit move
            
            self.board.make_move(move)

            self.turn = 'w' if self.turn == 'b' else 'b'
        
        self.game_data["result"] = self.checkmate if self.checkmate in ('w', 'b') else 't'
        return {"game_data": self.game_data, "result": self.checkmate if self.checkmate in ('w', 'b') else 't'}

    