from Move import Move
from Piece import Piece

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.char = 'k'

    def piece_to_filename(self):
        return self.color + 'k'

    def get_pseudo_legal_moves(self, board, special_moves=True):
        """
        Generate a list of pseudo-legal moves for the king piece.
        Pseudo-legal moves are moves that are legal according to the movement rules of the king,
        but do not take into account whether the king is moving into check.
        Args:
            board (Board): The current state of the chess board.
            check_castling (bool): If True, include castling moves in the list of valid moves.
        Returns:
            list: A list of tuples representing the valid target squares for the king.
        """
        
        pseudo_legal_moves: list[Move] = []
        row, col = self.position
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            target = (row + dr, col + dc)
            if board.is_within_bounds(target):
                if board.is_square_empty(target) or board.is_opponent_piece(target, self.color):
                    pseudo_legal_moves.append(Move(self.position, target, is_capture_move=True))
        
        if special_moves:
            # Castling logic integrated into get_legal_moves
            if self.color == 'w' and row == 7 and col == 4:
                # White castling rights are stored in 'KQ' for kingside and queenside
                white_kingside_empty = board.is_square_empty((7, 5)) and board.is_square_empty((7, 6))
                white_kingside_not_under_attack = not self.is_under_attack(board, (7, 4), 'w') and not self.is_under_attack(board, (7, 5), 'w')
                if 'K' in board.castling and white_kingside_empty and white_kingside_not_under_attack:
                    pseudo_legal_moves.append(Move(self.position, (7, 6), is_capture_move=False)) # Kingside castling move

                white_queenside_empty = board.is_square_empty((7, 1)) and board.is_square_empty((7, 2)) and board.is_square_empty((7, 3))
                white_queenside_not_under_attack = not self.is_under_attack(board, (7, 3), 'w') and not self.is_under_attack(board, (7, 4), 'w')
                if 'Q' in board.castling and white_queenside_empty and white_queenside_not_under_attack:
                    pseudo_legal_moves.append(Move(self.position, (7, 2), is_capture_move=False))  # Queenside castling move

            elif self.color == 'b' and row == 0 and col == 4:
                # Black castling rights are stored in 'kq' for kingside and queenside
                black_kingside_empty = board.is_square_empty((0, 5)) and board.is_square_empty((0, 6))
                black_kingside_not_under_attack = not self.is_under_attack(board, (0, 4), 'b') and not self.is_under_attack(board, (0, 5), 'b')
                if 'k' in board.castling and black_kingside_empty and black_kingside_not_under_attack:
                    pseudo_legal_moves.append(Move(self.position, (0, 6), is_capture_move=False))  # Kingside castling move

                black_queenside_empty = board.is_square_empty((0, 1)) and board.is_square_empty((0, 2)) and board.is_square_empty((0, 3))
                black_queenside_not_under_attack = not self.is_under_attack(board, (0, 3), 'b') and not self.is_under_attack(board, (0, 4), 'b')
                if 'q' in board.castling and black_queenside_empty and black_queenside_not_under_attack:
                    pseudo_legal_moves.append(Move(self.position, (0, 2), is_capture_move=False))  # Queenside castling move

        return pseudo_legal_moves

    def is_under_attack(self, board, square, color):
        # Check if a square is under attack by any opponent’s piece
        all_pseudo_legal_moves = board.get_all_attack_moves('w' if color == 'b' else 'b', special_moves=False)
        for move in all_pseudo_legal_moves:
            if move.end == square:
                return True
        return False
