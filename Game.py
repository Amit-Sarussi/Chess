from Board import Board
from Constants import *
from PlayerTypes import PlayerType
from RandomPlayer import RandomPlayer
from King import King
from Rook import Rook
from Move import Move

class Game:
    def __init__(self, player1=None, player2=None):
        self.board = Board(FEN_board=STARTING_FEN, color='w')
        self.turn = self.board.turn # 'w' or 'b'
        self.player1 = player1
        self.player2 = player2
        self.checkmate = None

    def make_move(self, move: Move, promotion=None):
        # Validate move
        # Check if piece owned by player:
        if self.board.is_opponent_piece(move.start, self.turn):
            return False, None, None
        
        # Is the movement in legal moves (Does not validate if king is in check!)?
        if move.end not in self.get_piece_legal_moves(move.start):
            return False, None, None

        # Validate the move does not put the king in check:
        if self.board.move_puts_king_in_check(move, self.turn):
            return False, None, None

        
        self.inspect_move(move)
        self.board.make_move(move)
        
        self.turn = 'w' if self.turn == 'b' else 'b'

        # Check if random player is in checkmate
        if len(self.board.get_possible_moves(self.turn)) == 0:
            self.checkmate = self.turn
            return True, move, self.checkmate
        
        # make random player move:
        move = self.random_player.get_player_move()
        self.inspect_move(move)
        self.board.make_move(move)
        self.turn = 'w' if self.turn == 'b' else 'b'
        
        # Check if player has available moves
        if len(self.board.get_possible_moves(self.turn)) == 0:
            self.checkmate = self.turn

        return True, move, self.checkmate

    def play(self):
        while self.checkmate == None:
            # Get move
            if self.turn == "w":
                move = self.player1.get_player_move()
            else:
                move = self.player2.get_player_move()

            while self.board.is_opponent_piece(move.start, self.turn) != True and move.end not in self.get_piece_legal_moves(move.start) != True and self.board.move_puts_king_in_check(move, self.turn) != True:
                # Get move
                if self.turn == "w":
                    move = self.player1.get_player_move()
                else:
                    move = self.player2.get_player_move()

            # Submit move
            self.inspect_move(move)
            self.board.make_move(move)

            self.turn = 'w' if self.turn == 'b' else 'b'

            # Check if random player is in checkmate
            if len(self.board.get_possible_moves(self.turn)) == 0:
                self.checkmate = self.turn
                return True, move, self.checkmate
        
        # Check if tie:
        if self.board.is_tie():
            self.game_history[-1].score = 0.5
            self.calculate_score()
            return 0, self.game_history
        
        if self.current_player_index == "x":
            self.game_history[-1].score = 1
            self.calculate_score()
            return 1, self.game_history
        
        self.game_history[-1].score = 0
        self.calculate_score()
        return 2, self.game_history
    
    def get_piece_legal_moves(self, position):
        piece = self.board.board[position]
        return piece.get_legal_moves(self.board)

    def inspect_move(self, move):
        start_square, end_square, promotion = move.get()
        piece = self.board.board[start_square]
        color = piece.color
        if isinstance(piece, King):
            self.board.castling = self.board.castling.replace('Q' if color == 'w' else 'q', '')
            self.board.castling = self.board.castling.replace('K' if color == 'w' else 'k', '')
        
        if isinstance(piece, Rook):
            if start_square[1] == 0 and start_square[0] == 0 and color == 'b':
                self.board.castling = self.board.castling.replace('q', '')
            if start_square[1] == 7 and start_square[0] == 0 and color == 'b':
                self.board.castling = self.board.castling.replace('k', '')
                
            if start_square[1] == 0 and start_square[0] == 7 and color == 'w':
                self.board.castling = self.board.castling.replace('Q', '')
            if start_square[1] == 7 and start_square[0] == 7 and color == 'w':
                self.board.castling = self.board.castling.replace('K', '')

        # Handle special case of castling move for King (update rook's position)
        if isinstance(piece, King):
            if color == 'w':
                if start_square == (7, 4) and end_square == (7, 2):  # White queenside castling
                    self.board.board[(7, 3)] = Rook('w', (7, 3))  # Place rook on queenside
                    self.board.board[(7, 0)] = None  # Remove rook from original position
                elif start_square == (7, 4) and end_square == (7, 6):  # White kingside castling
                    self.board.board[(7, 5)] = Rook('w', (7, 5))  # Place rook on kingside
                    self.board.board[(7, 7)] = None  # Remove rook from original position
            elif color == 'b':
                if start_square == (0, 4) and end_square == (0, 2):  # Black queenside castling
                    self.board.board[(0, 3)] = Rook('b', (0, 3))  # Place rook on queenside
                    self.board.board[(0, 0)] = None  # Remove rook from original position
                elif start_square == (0, 4) and end_square == (0, 6):  # Black kingside castling
                    self.board.board[(0, 5)] = Rook('b', (0, 5))  # Place rook on kingside
                    self.board.board[(0, 7)] = None  # Remove rook from original position
    
    