from turtle import position
from xmlrpc.client import boolean
import numpy as np
from Constants import *
from King import King
from Pawn import Pawn
from Move import Move
from Rook import Rook
import copy


class Board:
    def __init__(self, FEN_board, color='w'):
        self.FEN_board = FEN_board
        self.board, self.turn, self.castling, self.en_passant, self.halfmove, self.fullmove = self.FEN_to_board(FEN_board)
        self.white_pieces, self.black_pieces = self.get_pieces_list()
        self.color = color
        self.moves = []
    
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
    
    def board_to_FEN(self):
        board_str = ''
        for i in range(8):
            empty_count = 0
            for j in range(8):
                if self.board[i, j] is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        board_str += str(empty_count)
                    board_str += self.board[i, j].get_char()
                    empty_count = 0
            if empty_count > 0:
                board_str += str(empty_count)
            board_str += '/'
        board_str = board_str[:-1]

        FEN = board_str + " " + self.turn + " " + self.castling + " " + self.en_passant + " " + str(self.halfmove) + " " + str(self.fullmove)

        return FEN

    def get_pieces_list(self):
        white_pieces = [piece for i in range(8) for j in range(8) if (piece := self.board[i, j]) != None and piece.color == 'w']
        black_pieces = [piece for i in range(8) for j in range(8) if (piece := self.board[i, j]) != None and piece.color == 'b']
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
        # Update any missing data about the move:
        move.captured_piece = self.board[move.end]
        move.previous_castling = self.castling
        move.previous_en_passant = self.en_passant
        move.previous_halfmove = self.halfmove
        move.previous_fullmove = self.fullmove
        
        if self.board[move.start] == None: print("Start is none, from make_move")
        self.inspect_move(move)

        start, end, promotion = move.get()
        piece = self.board[start]
        self.board[start] = None

        if self.is_move_capture(move):
            self.halfmove = 0
        else:
            self.halfmove += 1
            
        self.moves.append(move.move_to_notation())
            
        if promotion is not None:
            piece = CHAR_TO_CLASS[promotion](piece.color, end)
        self.board[end] = piece
        piece.set_position(end)

        
        if self.turn == 'b':
            self.fullmove += 1

        self.turn = 'w' if self.turn == 'b' else 'b'
    
    def undo_move(self, move: Move):
        """
        Reverts the given move and restores the board state.
        """
        # Revert turn
        self.turn = 'w' if self.turn == 'b' else 'b'

        # Revert fullmove counter if black's turn
        if self.turn == 'b':
            self.fullmove -= 1

        # Revert halfmove, castling, en passant
        self.halfmove = move.previous_halfmove
        self.castling = move.previous_castling
        self.en_passant = move.previous_en_passant

        # Restore start and end squares
        start, end, promotion = move.get()
        piece = self.board[end]

        # Handle promotions
        if promotion is not None:
            # Revert the promoted piece back to a pawn
            piece = Pawn(piece.color, start)

        # Restore the moved piece to its original position
        piece.set_position(start)
        self.board[start] = piece
        self.board[end] = move.captured_piece  # Restore captured piece (if any)

        # Handle special cases: castling
        if isinstance(piece, King):
            if start == (7, 4) and end == (7, 2):  # White queenside castling
                self.board[(7, 0)] = Rook('w', (7, 0))
                self.board[(7, 3)] = None
            elif start == (7, 4) and end == (7, 6):  # White kingside castling
                self.board[(7, 7)] = Rook('w', (7, 7))
                self.board[(7, 5)] = None
            elif start == (0, 4) and end == (0, 2):  # Black queenside castling
                self.board[(0, 0)] = Rook('b', (0, 0))
                self.board[(0, 3)] = None
            elif start == (0, 4) and end == (0, 6):  # Black kingside castling
                self.board[(0, 7)] = Rook('b', (0, 7))
                self.board[(0, 5)] = None

        # Handle special cases: en passant
        if isinstance(piece, Pawn):
            if self.en_passant != "-" and end == Move.notation_to_position(self.en_passant):
                captured_pawn_pos = (end[0] + 1, end[1]) if piece.color == 'w' else (end[0] - 1, end[1])
                self.board[captured_pawn_pos] = Pawn('b' if piece.color == 'w' else 'w', captured_pawn_pos)
                self.board[end] = None

    def get_all_pseudo_legal_moves(self, color, special_moves=True):
        moves: list[Move] = []
        for piece in self.get_pieces_list()[0 if color == 'w' else 1]:
            if piece.color == color:
                moves.extend(piece.get_pseudo_legal_moves(self, special_moves))
        return moves

    def get_all_attack_moves(self, color, special_moves=True):
        pseudo_moves = self.get_all_pseudo_legal_moves(color, special_moves)
        for piece in self.get_pieces_list()[0 if color == 'w' else 1]:
            if isinstance(piece, Pawn):
                for move in piece.get_possible_captures(self):
                    pseudo_moves.append(move)
        return pseudo_moves
    
    def get_all_valid_moves(self, color):
        pseudo_legal_moves = self.get_all_pseudo_legal_moves(color)
        for move in pseudo_legal_moves:
            if self.board[move.start] is None: print("❌❌Start is none, in pseudo_legal_moves 1❌❌")
        # Filter the moves that put the king in check
        valid_moves = []
        for move in pseudo_legal_moves:
            if self.board[move.start] is None: print("❌❌Start is none, in pseudo_legal_moves 2❌❌")
            if self.validate_move(move, self.color):
                valid_moves.append(move)
                
        for move in valid_moves:
            if self.board[move.start] == None: print("❌❌Start is none, in valid_moves❌❌")

        return valid_moves

    def validate_move(self, move: Move, color, check_pseudo_legal=False, log=False) -> bool:
        """
        Validates a move on the board for the given color.
        
        Args:
            move (Move): The move to be validated.
            color (str): The color of the player making the move ('w' or 'b').
            check_pseudo_legal (bool): If True, checks if the move is pseudo-legal.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Check if the move is in the list of pseudo legal moves
        # if self.board[move.start] == None:
        #     if log: print(f"The piece at {move.start} is None")
        #     return False
        
        if check_pseudo_legal:
            piece = self.board[move.start]
            pseudo_legal_moves = piece.get_pseudo_legal_moves(self)
            if move not in pseudo_legal_moves:
                if log: print(f"Move {move} is not pseudo-legal")
                return False
            
        # Check if piece owned by player:
        if self.is_opponent_piece(move.start, self.turn):
            if log: print(f"The piece at {move.start} is not owned by {self.turn}")
            return False
        
        # Check if the move puts the king in check
        if self.board[move.start] == None: print("Start is none, from validate_move")
        if self.move_puts_king_in_check(move, self.turn):
            if log: print(f"Move {move} puts your king in check")
            return False
        
        return True 

    def is_move_capture(self, move: Move):
        start, end, promotion = move.get()
        return not self.is_square_empty(end)
    
    def is_move_promotion(self, move: Move):
        start, end, promotion = move.get()
        piece = self.board[start]
        return isinstance(piece, Pawn) and (end[0] == 0 or end[0] == 7)
    
    def is_king_in_check(self, color):
        king_position = None
        for piece in self.get_pieces_list()[0 if color == 'w' else 1]:
            if isinstance(piece, King):
                king_position = piece.position
                break
        
        if king_position is None:
            raise ValueError(f"No king found for color {color}")
        
        opponent_color = 'b' if color == 'w' else 'w'
        opponent_moves = self.get_all_pseudo_legal_moves(opponent_color)
        
        for move in opponent_moves:
            if move.end == king_position:
                return True
        return False

    def move_puts_king_in_check(self, move: Move, color) -> bool:
        if self.board[move.start] == None: print("Start is none, from move_puts_king_in_check")
        before = self.board_to_FEN()
        self.make_move(move)
        is_in_check = False
        if self.is_king_in_check(color):
            is_in_check = True
        self.undo_move(move)
        if self.board_to_FEN() != before:
            print(f"Error in undo move:\nbefore: {before}\nafter: {self.board_to_FEN()}\nmove: {move}")
        return is_in_check
    
    def inspect_move(self, move: Move):
        if self.board[move.start] == None: 
            print("Start is none, from insepct_move")
            print(move)
            print(self.board)
            print(self.board[move.start])
            print(self.board_to_FEN())
        start_square, end_square, promotion = move.get()
        piece = self.board[start_square]
        color = piece.color
        
        # Handle special case of castling move for King
        if isinstance(piece, King):
            self.castling = self.castling.replace('Q' if color == 'w' else 'q', '')
            self.castling = self.castling.replace('K' if color == 'w' else 'k', '')
        
        # Handle special case of castling move for Rook
        if isinstance(piece, Rook):
            if start_square[1] == 0 and start_square[0] == 0 and color == 'b':
                self.castling = self.castling.replace('q', '')
            if start_square[1] == 7 and start_square[0] == 0 and color == 'b':
                self.castling = self.castling.replace('k', '')
                
            if start_square[1] == 0 and start_square[0] == 7 and color == 'w':
                self.castling = self.castling.replace('Q', '')
            if start_square[1] == 7 and start_square[0] == 7 and color == 'w':
                self.castling = self.castling.replace('K', '')
        
        # Check if one of the rooks is being captured during this move and update castling accordingly
        captured_piece = self.board[move.end]
        if isinstance(captured_piece, Rook):
            # Get the color of the captured rook:
            color = captured_piece.color
            if color == "w":
                # Check if castling is even possible (Maybe nothing needs to change)
                if "K" in self.castling and move.end == (7, 7):
                    self.castling = self.castling.replace("K", "")
                if "Q" in self.castling and move.end == (7, 0):
                    self.castling = self.castling.replace("Q", "")
            elif color == "b":
                # Check if castling is even possible (Maybe nothing needs to change)
                if "k" in self.castling and move.end == (0, 7):
                    self.castling = self.castling.replace("k", "")
                if "q" in self.castling and move.end == (0, 0):
                    self.castling = self.castling.replace("q", "")
                    
        if self.castling == "": self.castling = "-"

        # Handle special case of castling move for King (update rook's position)
        if isinstance(piece, King):
            if color == 'w':
                if start_square == (7, 4) and end_square == (7, 2):  # White queenside castling
                    self.board[(7, 3)] = Rook('w', (7, 3))  # Place rook on queenside
                    self.board[(7, 0)] = None  # Remove rook from original position
                elif start_square == (7, 4) and end_square == (7, 6):  # White kingside castling
                    self.board[(7, 5)] = Rook('w', (7, 5))  # Place rook on kingside
                    self.board[(7, 7)] = None  # Remove rook from original position
            elif color == 'b':
                if start_square == (0, 4) and end_square == (0, 2):  # Black queenside castling
                    self.board[(0, 3)] = Rook('b', (0, 3))  # Place rook on queenside
                    self.board[(0, 0)] = None  # Remove rook from original position
                elif start_square == (0, 4) and end_square == (0, 6):  # Black kingside castling
                    self.board[(0, 5)] = Rook('b', (0, 5))  # Place rook on kingside
                    self.board[(0, 7)] = None  # Remove rook from original position

        # En passant:
        color = piece.color
        # Check if move is pawn double move and update en passant accordingly:
        if isinstance(piece, Pawn):
            # check if move is double move
            if start_square[1] == end_square[1] and abs(start_square[0] - end_square[0]) == 2:
                # calculate square before en passant
                if color == 'w':
                    en_passant_square = (end_square[0] + 1, end_square[1])
                    self.en_passant = Move.position_to_notation(en_passant_square)
                elif color == 'b':
                    en_passant_square = (end_square[0] - 1, end_square[1])
                    self.en_passant = Move.position_to_notation(en_passant_square)
            else:
                if self.en_passant != "-" and end_square == Move.notation_to_position(self.en_passant):
                    # remove the pawn that was captured by en passant
                    if self.turn == 'w':
                        self.board[(end_square[0] + 1, end_square[1])] = None
                    elif self.turn == 'b':
                        self.board[(end_square[0] - 1, end_square[1])] = None
                        
                self.en_passant = "-"
        else:
            self.en_passant = "-"



