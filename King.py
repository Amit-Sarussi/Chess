from Piece import Piece

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def piece_to_filename(self):
        return self.color + 'k'

    def get_legal_moves(self, board):
        valid_moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            target = (row + dr, col + dc)
            if board.is_within_bounds(target):
                if board.is_square_empty(target) or board.is_opponent_piece(target, self.color):
                    valid_moves.append(target)
        
        # Castling logic integrated into get_legal_moves
        if self.color == 'w' and row == 7 and col == 4:
            # White castling rights are stored in 'KQ' for kingside and queenside
            if 'K' in board.castling and board.is_square_empty((7, 5)) and board.is_square_empty((7, 6)) and not self.is_under_attack(board, (7, 4), 'w') and not self.is_under_attack(board, (7, 5), 'w'):
                valid_moves.append((7, 6))  # Kingside castling move

            if 'Q' in board.castling and board.is_square_empty((7, 1)) and board.is_square_empty((7, 2)) and board.is_square_empty((7, 3)) and not self.is_under_attack(board, (7, 4), 'w') and not self.is_under_attack(board, (7, 3), 'w'):
                valid_moves.append((7, 2))  # Queenside castling move

        elif self.color == 'b' and row == 0 and col == 4:
            # Black castling rights are stored in 'kq' for kingside and queenside
            if 'k' in board.castling and board.is_square_empty((0, 5)) and board.is_square_empty((0, 6)) and not self.is_under_attack(board, (0, 4), 'b') and not self.is_under_attack(board, (0, 5), 'b'):
                valid_moves.append((0, 6))  # Kingside castling move

            if 'q' in board.castling and board.is_square_empty((0, 1)) and board.is_square_empty((0, 2)) and board.is_square_empty((0, 3)) and not self.is_under_attack(board, (0, 4), 'b') and not self.is_under_attack(board, (0, 3), 'b'):
                valid_moves.append((0, 2))  # Queenside castling move

        return valid_moves

    def is_under_attack(self, board, square, color):
    # Check if a square is under attack by any opponent’s piece
        for i in range(8):
            for j in range(8):
                piece = board.board[i, j]
                if piece and piece.color != color:
                    # Check if the opponent's piece can legally move to the square
                    if square in piece.get_legal_moves(board):
                        return True
        return False
