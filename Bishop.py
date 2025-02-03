from Piece import Piece

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.char = 'b'
    
    def piece_to_filename(self):
        return self.color + 'b'

    def get_pseudo_legal_moves(self, board, special_moves=True):
        """
        Calculate all pseudo-legal moves for the bishop from its current position.
        Pseudo-legal moves are moves that the bishop can make according to its movement
        rules, without considering whether the move would put the player's king in check.
        Args:
            board (Board): The current state of the chess board.
        Returns:
            list: A list of tuples representing the coordinates of all valid pseudo-legal moves. (Only the end of the move is returned)
        """
        
        pseudo_legal_moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_within_bounds((r, c)):
                if board.is_square_empty((r, c)):
                    pseudo_legal_moves.append((r, c))
                elif board.is_opponent_piece((r, c), self.color):
                    pseudo_legal_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

        move_converted = [self.convert_move(self.position, move) for move in pseudo_legal_moves]
        return move_converted
