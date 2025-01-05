from Piece import Piece

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def piece_to_filename(self):
        return self.color + 'b'

    def get_legal_moves(self, board):
        valid_moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_within_bounds((r, c)):
                if board.is_square_empty((r, c)):
                    valid_moves.append((r, c))
                elif board.is_opponent_piece((r, c), self.color):
                    valid_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

        return valid_moves
