from Move import Move
from Piece import Piece

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.char = 'n'
    
    def piece_to_filename(self):
        return self.color + 'n'

    def get_pseudo_legal_moves(self, board, special_moves=True):
        """
        Calculate and return a list of pseudo-legal moves for the knight.
        A pseudo-legal move is a move that the knight can make according to its movement rules,
        regardless of whether it would put the player's own king in check.
        Args:
            board (Board): The current state of the chess board.
        Returns:
            list: A list of tuples representing the target positions (row, col) 
                  that the knight can move to.
        """
        
        pseudo_legal_moves: list[Move] = []
        row, col = self.position
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dr, dc in knight_moves:
            target = (row + dr, col + dc)
            if board.is_within_bounds(target):
                if board.is_square_empty(target) or board.is_opponent_piece(target, self.color):
                    pseudo_legal_moves.append(Move(self.position, target, is_capture_move=True))
        
        return pseudo_legal_moves
