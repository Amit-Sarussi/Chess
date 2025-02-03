from Move import Move
from Piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.char = 'r'
 
    def piece_to_filename(self):
        return self.color + 'r'

    def get_pseudo_legal_moves(self, board, special_moves=True):
        """
        Calculate and return all pseudo-legal moves for the rook on the given board.
        Pseudo-legal moves are moves that the rook can make according to its movement
        rules, without considering checks or pins.
        Args:
            board (Board): The current state of the chess board.
        Returns:
            list of tuple: A list of tuples representing the coordinates of all valid
            pseudo-legal moves for the rook. Each tuple contains two integers (row, col).
        """
        
        pseudo_legal_moves: list[Move] = []
        row, col = self.position

        # Rook moves horizontally and vertically
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

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
