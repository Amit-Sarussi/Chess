from Piece import Piece

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def piece_to_filename(self):
        return self.color + 'n'

    def get_legal_moves(self, board):
        valid_moves = []
        row, col = self.position
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dr, dc in knight_moves:
            target = (row + dr, col + dc)
            if board.is_within_bounds(target):
                if board.is_square_empty(target) or board.is_opponent_piece(target, self.color):
                    valid_moves.append(target)
        
        return valid_moves
