import numpy as np
from Constants import *
from King import King
from Pawn import Pawn
from Move import Move
import copy


class Board:
    def __init__(self, FEN_board, color='w'):
        self.FEN_board = FEN_board
        self.board, self.turn, self.castling, self.en_passant, self.halfmove, self.fullmove = self.FEN_to_board(FEN_board)
        self.white_pieces, self.black_pieces = self.get_pieces_list()
        self.color = color
    
    def copy(self):
        board_copy = Board(self.FEN_board, self.color)
        board_copy.board = copy.deepcopy(self.board)
        board_copy.turn = self.turn
        board_copy.castling = self.castling
        board_copy.en_passant = self.en_passant
        board_copy.halfmove = self.halfmove
        board_copy.fullmove = self.fullmove
        board_copy.white_pieces = self.white_pieces.copy()
        board_copy.black_pieces = self.black_pieces.copy()
        
        return board_copy
        
    def FEN_to_board(self, FEN_board):
        fields = FEN_board.split()
        board = np.full((8, 8), None, dtype=object)
        rows = fields[0].split('/')
        for i, row in enumerate(rows):
            col = 0
            for char in row:
                if char.isdigit():
                    col += int(char)
                else:
                    board[i, col] = CHAR_TO_CLASS[char.lower()]('w' if char.isupper() else 'b', (i, col))
                    col += 1
        return board, fields[1], fields[2], fields[3], int(fields[4]), int(fields[5])

    def get_pieces_list(self):
        white_pieces = [(piece, (i, j)) for i in range(8) for j in range(8) if (piece := self.board[i, j]) != None and piece.color == 'w']
        black_pieces = [(piece, (i, j)) for i in range(8) for j in range(8) if (piece := self.board[i, j]) != None and piece.color == 'b']
        return white_pieces, black_pieces

    def is_square_empty(self, position):
        row, col = position
        return self.board[row, col] is None

    def is_opponent_piece(self, position, color):
        """Checks if the square contains an opponent's piece."""
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.board[row, col]
            if piece is not None:
                if color == 'w':
                    return piece.color == 'b'
                else:
                    return piece.color == 'w'
        return False

    def is_within_bounds(self, position):
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8
    
    def make_move(self, move: Move):
        start, end, promotion = move.get()
        piece = self.board[start]
        self.board[start] = None

        if promotion is not None:
            piece = CHAR_TO_CLASS[promotion](piece.color, end)
        self.board[end] = piece
        piece.set_position(end)

        if self.is_move_capture(move):
            self.halfmove = 0
        else:
            self.halfmove += 1
        
        if self.turn == 'b':
            self.fullmove += 1

        self.turn = 'w' if self.turn == 'b' else 'b'

    
    def get_possible_moves(self, color):
        moves: list[Move] = []
        for piece, position in self.get_pieces_list()[0 if color == 'w' else 1]:
            if piece.color == color:
                moves.extend([Move(position,x) for x in piece.get_legal_moves(self)])
        return moves

    def is_move_capture(self, move: Move):
        start, end, promotion = move.get()
        return not self.is_square_empty(end)
    
    def is_move_promotion(self, move: Move):
        start, end, promotion = move.get()
        piece = self.board[start]
        return isinstance(piece, Pawn) and (end[0] == 0 or end[0] == 7)
    
    def is_king_in_check(self, color):
        king_position = None
        for piece, position in self.get_pieces_list()[0 if color == 'w' else 1]:
            if isinstance(piece, King):
                king_position = position
                break
        
        if king_position is None:
            raise ValueError(f"No king found for color {color}")
        
        opponent_color = 'b' if color == 'w' else 'w'
        opponent_moves = self.get_possible_moves(opponent_color)
        
        for move in opponent_moves:
            if move.end == king_position:
                return True
        return False

    def move_puts_king_in_check(self, move: Move, color):
        board_copy = self.copy()
        board_copy.make_move(move)
        return board_copy.is_king_in_check(color)



