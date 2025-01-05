from Piece import Piece

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def set_position(self, new_position):
        self.position = new_position
    
    def piece_to_filename(self):
        return self.color + 'p'

    def get_legal_moves(self, board):
        valid_moves = []
        row, col = self.position
        direction = -1 if self.color == 'w' else 1  # White moves up (-1), Black moves down (+1)
        
        # Normal move
        if board.is_within_bounds((row + direction, col)) and board.is_square_empty((row + direction, col)):
            valid_moves.append((row + direction, col))
            # Double move
            if self.is_first_move() and board.is_within_bounds((row + 2 * direction, col)):
                if board.is_square_empty((row + 2 * direction, col)):
                    valid_moves.append((row + 2 * direction, col))
        
        # Captures
        for dc in [-1, 1]:
            target = (row + direction, col + dc)
            if board.is_within_bounds(target) and board.is_opponent_piece(target, self.color):
                valid_moves.append(target)
        
        return valid_moves

    def is_first_move(self):
        return self.position[0] == 6 if self.color == 'w' else self.position[0] == 1        
    
    # En Passant
    # if board.en_passant != '-':
    #     en_passant_target = (8 - int(board.en_passant[1]), ord(board.en_passant[0]) - ord('a'))
    #     if en_passant_target == (row + direction, col - 1) or en_passant_target == (row + direction, col + 1):
    #         valid_moves.append(en_passant_target)