from Board import Board
from Constants import *
from RandomPlayer import RandomPlayer
from King import King
from Rook import Rook

class Game:
    def __init__(self):
        self.board = Board(FEN_board=STARTING_FEN, color='w')
        self.turn = self.board.turn # 'w' or 'b'
        self.random_player = RandomPlayer(self.board, 'b')

    def make_move(self, move, promotion=None): # move: ((1,1), (3,1)) or ((1,1), (2,1))
      # Validate move
        # Check if piece owned by player:
        if self.board.is_opponent_piece(move[0], self.turn):
            return False, None
        
        # Is the movement in legal moves (Does not validate if king is in check!)?
        if move[1] not in self.get_piece_legal_moves(move[0]):
            return False, None

        # Validate the move does not put the king in check:
        if self.board.move_puts_king_in_check(*move, self.turn):
            return False, None

        
        self.inspect_move(move)
        self.board.make_move(move)
        
        self.turn = 'w' if self.turn == 'b' else 'b'
        
        # make random player move:
        move = self.random_player.get_player_move()
        self.inspect_move(move)
        self.board.make_move(move)
        self.turn = 'w' if self.turn == 'b' else 'b'
        return True, move

    
    def get_piece_legal_moves(self, position):
        piece = self.board.board[position]
        return piece.get_legal_moves(self.board)

    def inspect_move(self, move):
        start_square, end_square = move
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
    
    