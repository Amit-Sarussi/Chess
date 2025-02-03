from Piece import Piece
from Move import Move
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.char = 'p'

    def set_position(self, new_position):
        self.position = new_position
    
    def piece_to_filename(self):
        return self.color + 'p'

    def get_pseudo_legal_moves(self, board, special_moves=True):
        """
        Generate a list of pseudo-legal moves for the pawn.
        Pseudo-legal moves are moves that a pawn can make according to the rules of chess,
        without considering whether the move would leave the king in check.
        Args:
            board (Board): The current state of the chess board.
        Returns:
            list: A list of tuples representing the pseudo-legal moves. Each tuple contains
                  the target row and column, and optionally the promotion piece ('q', 'r', 'b', 'n')
                  if the move is a promotion.
        """
        
        pseudo_legal_moves: list[Move] = []
        row, col = self.position
        direction = -1 if self.color == 'w' else 1  # White moves up (-1), Black moves down (+1)
        
        # Normal move
        if board.is_within_bounds((row + direction, col)) and board.is_square_empty((row + direction, col)):
            # Check if promotion
            if board.is_move_promotion(Move(self.position, (row + direction, col))):
                for promotion in ['q', 'r', 'b', 'n']:
                    pseudo_legal_moves.append(Move(self.position, (row + direction, col), promotion=promotion, is_capture_move=False))
    
            # If not promotion and just normal move
            else:
                pseudo_legal_moves.append(Move(self.position, (row + direction, col), is_capture_move=False))
            # Double move
            if self.is_first_move() and board.is_within_bounds((row + 2 * direction, col)):
                if board.is_square_empty((row + 2 * direction, col)):
                    pseudo_legal_moves.append(Move(self.position, (row + 2 * direction, col), is_capture_move=False))
        
        # Captures
        for dc in [-1, 1]:
            target = (row + direction, col + dc)
            if board.is_within_bounds(target) and board.is_opponent_piece(target, self.color):
                # Check if promotion
                if board.is_move_promotion(Move(self.position, target)):
                    for promotion in ['q', 'r', 'b', 'n']:
                        pseudo_legal_moves.append(m:=Move(self.position, target, promotion=promotion, is_capture_move=True))
                # If not promotion
                else:
                    pseudo_legal_moves.append(Move(self.position, target, is_capture_move=True))
        
        # En Passant
        if board.en_passant != '-':
            letters = "abcdefgh"
            en_passant_target = (8-int(board.en_passant[1]), letters.index(board.en_passant[0]))
            if en_passant_target == (row + direction, col - 1) or en_passant_target == (row + direction, col + 1):
                pseudo_legal_moves.append(Move(self.position, en_passant_target, is_capture_move=False))
        
        return pseudo_legal_moves

    def is_first_move(self):
        return self.position[0] == 6 if self.color == 'w' else self.position[0] == 1
    
    def get_possible_captures(self, board):
        direction = -1 if self.color == 'w' else 1
        captures = []
        for dc in [-1, 1]:
            target = (self.position[0] + direction, self.position[1] + dc)
            if board.is_within_bounds(target) and (board.is_opponent_piece(target, self.color) or board.is_square_empty(target)):
                captures.append(Move(self.position, target))
        return captures        
    
    
   