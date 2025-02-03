from Move import Move
from Piece import Piece

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.char = 'q'
        
    def piece_to_filename(self):
        return self.color + 'q'

    def get_pseudo_legal_moves(self, board, special_moves=True):
        """
        Calculate pseudo-legal moves for the queen piece on the given board.
        Pseudo-legal moves are all possible moves the queen can make without considering checks.
        Args:
            board (Board): The current state of the chess board.
        Returns:
            List[Tuple[int, int]]: A list of tuples representing the valid moves for the queen.
        """
        
        pseudo_legal_moves: list[Move] = []
        row, col = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # All 8 possible directions

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_within_bounds((r, c)):
                if board.is_square_empty((r, c)):
                    pseudo_legal_moves.append(Move(self.position, (r, c), is_capture_move=True))
                elif board.is_opponent_piece((r, c), self.color):
                    pseudo_legal_moves.append(Move(self.position, (r, c), is_capture_move=True))
                    break
                else:
                    break
                r += dr
                c += dc

        return pseudo_legal_moves
