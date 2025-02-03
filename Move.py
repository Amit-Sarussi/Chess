
class Move:
    def __init__(self, start, end, promotion=None, is_capture_move=True, captured_piece=None, previous_castling=None, previous_en_passant=None, previouse_halfmove=None, previous_fullmove=None):
        self.start = start
        self.end = end
        self.promotion = promotion
        self.is_capture_move = is_capture_move
        self.captured_piece = captured_piece
        self.previous_castling = previous_castling
        self.previous_en_passant = previous_en_passant
        self.previous_halfmove = previouse_halfmove
        self.previous_fullmove = previous_fullmove
    
    def copy(self):
        return Move(self.start, self.end, self.promotion, self.is_capture_move, self.captured_piece, self.previous_castling, self.previous_en_passant, self.previous_halfmove, self.previous_fullmove)
    
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.start == other.start and self.end == other.end and self.promotion == other.promotion

    def __str__(self):
        return f"{self.start} -> {self.end}, {self.promotion}"
    
    def get(self):
        return self.start, self.end, self.promotion

    def move_to_notation(self):
        start = Move.position_to_notation(self.start)
        end = Move.position_to_notation(self.end)
        return start + end + (self.promotion if self.promotion != None else "")
    
    @staticmethod
    def notation_to_move(notation):
        start_square = notation[0:2]
        end_square = notation[2:4]
        start = Move.notation_to_position(start_square)
        end = Move.notation_to_position(end_square)
        if len(notation) > 4:
            promotion = notation[4]
        else:
            promotion = None
        return Move(start, end, promotion=promotion)
    
    @staticmethod
    def position_to_notation(position):
        letters = "abcdefgh"
        row, col = position
        return letters[col] + str(8-row)
    
    @staticmethod
    def notation_to_position(notation):
        letters = "abcdefgh"
        row = 8-int(notation[1])
        col = letters.index(notation[0])
        return (row, col)
        