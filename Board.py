from Constants import *
from Move import encode_move, decode_move
from PreComputer import create_bishop_lookup_table, create_rook_lookup_table, generate_attacks, generate_masks
import chess

class Board:
    def __init__(self, starting_fen: str) -> None:
        self.starting_fen = starting_fen
        self.bitboards = {color + "_" + piece: 0 for color in ["white", "black"] for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]}
        turn, self.castling, self.en_passant, self.halfmove, self.fullmove = self.convert_from_fen(starting_fen)
        self.turn = "white" if turn == "w" else "black"
        self.moves = []
        self.attacks = generate_attacks()
        self.masks = generate_masks()
        self.rook_lookup = create_rook_lookup_table()
        self.bishop_lookup = create_bishop_lookup_table()
        self.update_color_bitboards()
        self.update_attack_bitboards()
    
    def convert_from_fen(self, FEN) -> tuple[str, str, str, int, int]:
        fields = FEN.split()
        ranks = fields[0].split('/')

        piece_names = ["pawn", "knight", "bishop", "rook", "queen", "king"]

        for rank_index, rank_str in enumerate(ranks):
            file_index = 0
            for char in rank_str:
                if char.isdigit():
                    file_index += int(char)
                else:
                    piece_type = piece_names["pnbrqk".index(char.lower())]
                    color = "white_" if char.isupper() else "black_"
                    square = (7 - rank_index) * 8 + file_index
                    self.bitboards[color + piece_type] |= (1 << square)
                    file_index += 1

        en_passant = -1 if fields[3] == "-" else self.notation_to_square(fields[3])
        
        return fields[1], fields[2], en_passant, int(fields[4]), int(fields[5])
    
    def convert_to_fen(self) -> str:
        fen = ""
        
        # Iterate over each rank from 8 to 1
        for rank in range(7, -1, -1):
            rank_str = ""
            empty_count = 0
            
            # For each file from a to h
            for file in range(8):
                square = rank * 8 + file
                piece_found = False
                
                # Check every piece in our bitboards.
                for color in ["white", "black"]:
                    for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                        bitboard = self.bitboards.get(f"{color}_{piece}", 0)
                        if bitboard & (1 << square):
                            # If there were empty squares before, append that count.
                            if empty_count > 0:
                                rank_str += str(empty_count)
                                empty_count = 0
                            # Use the mapping: uppercase for white, lowercase for black.
                            char = PIECE_TO_CHAR[piece]
                            rank_str += char.upper() if color == "white" else char.lower()
                            piece_found = True
                            break
                    if piece_found:
                        break
                
                if not piece_found:
                    empty_count += 1
            
            # Append any trailing empty squares.
            if empty_count > 0:
                rank_str += str(empty_count)
            
            fen += rank_str + "/"
            
        en_passant = "-" if self.en_passant == -1 else self.square_to_notation(self.en_passant)
        turn = "w" if self.turn == "white" else "b"
        fen = f"{fen.rstrip("/")} {turn} {self.castling} {en_passant} {self.halfmove} {self.fullmove}"
        
        return fen

    def notation_to_square(self, notation):
        file = ord(notation[0]) - ord('a')
        rank = int(notation[1]) - 1
        return rank * 8 + file
    
    def square_to_notation(self, square):
        file = chr(ord('a') + (square % 8))
        rank = (square // 8) + 1  # since bit 0 is a1, rank 1
        return f"{file}{rank}"

    def update_color_bitboards(self) -> None:
        for color in ["white", "black"]:
            self.bitboards[color] = 0
            for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                self.bitboards[color] |= self.bitboards[f"{color}_{piece}"]
        
    def update_attack_bitboards(self) -> None:
        self.bitboards["white_attacks"] = self.calculate_attacks("white")
        self.bitboards["black_attacks"] = self.calculate_attacks("black")
        
    def calculate_attacks(self, color):
        attacks = 0
        for piece_type in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
            pieces = self.bitboards[f"{color}_{piece_type}"]
            while pieces:
                square = self.bsf(pieces)
                if piece_type == "queen":
                    attacks |= self.get_bishop_attacks(square) | self.get_rook_attacks(square)
                elif piece_type == "bishop":
                    attacks |= self.get_bishop_attacks(square)
                elif piece_type == "rook":
                    attacks |= self.get_rook_attacks(square)
                elif piece_type == "king":
                    attacks |= self.attacks["king"][square]
                elif piece_type == "knight":
                    attacks |= self.attacks["knight"][square]
                elif piece_type == "pawn":
                    attacks |= self.attacks[f"{color}_pawn_attacks"][square]

                pieces &= ~(1 << square)
        return attacks
    
    def is_square_empty(self, square) -> bool:
        occupied = self.bitboards["white"] | self.bitboards["black"]
        return (occupied & (1 << square)) == 0
    
    def is_opponent(self, square, color) -> bool:
        opponent = "black" if color == "white" else "white"
        return (self.bitboards[opponent] & (1 << square)) != 0

    def make_move(self, move: str):
        move_data = {"move": move, "captured_piece": None, "previous_castling": self.castling, "previous_en_passant": self.en_passant, "previous_halfmove": self.halfmove, "previous_fullmove": self.fullmove}
        
        self.process_move_updates(move)
        start, end, promotion = decode_move(move)
        color = "white" if self.turn == "white" else "black"
        other_color = "white" if color == "black" else "black"
        
        self.moves.append(move_data)
        
        # Reset every capture or pawn advance
        if self.bitboards[other_color] & (1 << end) != 0 or self.bitboards[f"{color}_pawn"] & (1 << start) != 0:
            self.halfmove = 0
        else:
            self.halfmove += 1
        
        # Remove captured opponent piece (if any)
        for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
            if self.bitboards[f"{other_color}_{piece}"] & (1 << end):
                move_data["captured_piece"] = f"{other_color}_{piece}"
                self.remove_piece(f"{other_color}_{piece}", end)
                break
        
        
        if promotion != 0:
            promotion_table = ["queen", "rook", "bishop", "knight"]
            promotion_piece = promotion_table[promotion - 1]
            self.remove_piece(f"{color}_pawn", start)
            self.add_piece(f"{color}_{promotion_piece}", end)
        else:
            # Determine which piece is moving
            for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                if self.bitboards[f"{color}_{piece}"] & (1 << start):
                    self.move_piece(f"{color}_{piece}", start, end)
                    break
        
        if self.turn == 'b':
            self.fullmove += 1

        self.turn = 'white' if self.turn == 'black' else 'black'
    
    def undo_move(self):
        # Revert turn
        self.turn = 'white' if self.turn == 'black' else 'black'

        # Revert fullmove counter if black's turn
        if self.turn == 'b':
            self.fullmove -= 1

        move_data = self.moves.pop()

        # Revert halfmove, castling, en passant
        self.halfmove = move_data["previous_halfmove"]
        self.castling = move_data["previous_castling"]
        self.en_passant = move_data["previous_en_passant"]

        start, end, promotion = decode_move(move_data["move"])

        if promotion != 0:
            promotion_table = ["queen", "rook", "bishop", "knight"]
            promotion_piece = promotion_table[promotion - 1]
            self.remove_piece(f"{self.turn}_{promotion_piece}", end)
            self.add_piece(f"{self.turn}_pawn", start)
        else:
            for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                if self.bitboards[f"{self.turn}_{piece}"] & (1 << end):
                    self.move_piece(f"{self.turn}_{piece}", end, start)
                    break
                
            # Revert captured opponent piece (if any)
            if move_data["captured_piece"] is not None:
                self.add_piece(move_data["captured_piece"], end)

        # Handle castling (If piece is king then move the rook back)
        if self.bitboards[f"{self.turn}_king"] & (1 << start) != 0:
            self.unperform_castling_rook_move(self.turn, start, end)

        # Handle en passant (Add the captured pawn)
        if self.bitboards[f"{self.turn}_pawn"] & (1 << start) and end == self.en_passant:
            self.unperform_en_passant(self.turn, start, end)
        
    def process_move_updates(self, move: str) -> None:   
        start, end, promotion = decode_move(move)
        color = "white" if self.turn == "w" else "black"
        other_color = "white" if color == "black" else "black"
        
        if self.castling != "-":
            # Check if king moved and remove castling rights
            if self.bitboards[f"{color}_king"] & (1 << start) != 0:
                self.castling = self.castling.replace("K" if color == "white" else "k", "")
                self.castling = self.castling.replace("Q" if color == "white" else "q", "")
            
            # Check if rook moved and remove castling rights
            if self.bitboards[f"{color}_rook"] & (1 << start) != 0:
                if start == 7 and color == "white":
                    self.castling = self.castling.replace('K', "")
                if start == 0 and color == "white":
                    self.castling = self.castling.replace('Q', "")
                if start == 63 and color == "black":
                    self.castling = self.castling.replace('k', "")
                if start == 56 and color == "black":
                    self.castling = self.castling.replace('q', "")
            
            # Check if rook got eaten and remove castling rights
            if self.bitboards[f"{other_color}_rook"] & (1 << end) != 0:
                if end == 7 and other_color == "white":
                    self.castling = self.castling.replace('K', "")
                if end == 0 and other_color == "white":
                    self.castling = self.castling.replace('Q', "")
                if end == 63 and other_color == "black":
                    self.castling = self.castling.replace('k', "")
                if end == 56 and other_color == "black":
                    self.castling = self.castling.replace('q', "")
            
            # If castling update rook position
            self.perform_castling_rook_move(color, start, end)
            
            if self.castling == "": self.castling = "-"
        
        # Check if en passant update
        direction = 1 if color == "white" else -1
        if self.bitboards[f"{color}_pawn"] & (1 << start) != 0:
            if end - start == 16 * direction:  # Double pawn move
                self.en_passant = start + 8 * direction  # En passant target square calculation
            elif end == self.en_passant:  # En passant capture
                self.remove_piece(f"{other_color}_pawn", self.en_passant - 8 * direction)  # Captured pawn square
                self.en_passant = -1  # Reset after capture
            else:
                self.en_passant = -1  # Reset if not a double move or en passant capture
        else:
            self.en_passant = -1 # Reset if not a pawn move.

    def perform_castling_rook_move(self, color, start, end):
        if color == "white":
            if start == 4 and end == 2:
                self.move_piece("white_rook", 0, 3)  # Queenside castling
            elif start == 4 and end == 6:
                self.move_piece("white_rook", 7, 5)  # Kingside castling
        elif color == "black":
            if start == 60 and end == 58:
                self.move_piece("black_rook", 56, 59)  # Queenside castling
            elif start == 60 and end == 62:
                self.move_piece("black_rook", 63, 61)  # Kingside castling

    def unperform_castling_rook_move(self, color, start, end):
        if color == "white":
            if start == 4 and end == 2:
                self.move_piece("white_rook", 3, 0)  # Queenside castling
            elif start == 4 and end == 6:
                self.move_piece("white_rook", 5, 7)  # Kingside castling
        elif color == "black":
            if start == 60 and end == 58:
                self.move_piece("black_rook", 59, 56)  # Queenside castling
            elif start == 60 and end == 62:
                self.move_piece("black_rook", 61, 63)  # Kingside castling

    def unperform_en_passant(self, color, start, end):
        captured_square = end - 8 if color == "white" else end + 8
        other_color = "white" if color == "black" else "black"
        self.add_piece(f"{other_color}_pawn", captured_square)
    
    def is_attacking(self, square, color):
        return self.bitboards[f"{color}_attacks"] & (1 << square) != 0
    
    def move_puts_king_in_check(self, move, color):
        is_in_check = False
        self.make_move(move)

        kings = self.bitboards[f"{color}_king"]  # Use the original color!
        king_square = self.bsf(kings)
        other_color = "white" if color == "black" else "black"

        if self.is_attacking(king_square, other_color):
            is_in_check = True

        self.undo_move()
        return is_in_check
    
    def validate_move(self, move: str, color, check_pseudo_legal=False):
        # Check that move is pseudo_legal
        if check_pseudo_legal:
            if move not in self.get_all_pseudo_legal_moves(color):
                return False
            
        # Check that it dont puts the king in check
        if self.move_puts_king_in_check(move, color):
            return False
        
        return True
           
    def generate_moves_for_piece(self, piece_type, color):
        moves = []
        bitboard = self.bitboards[f"{color}_{piece_type}"]
        
        while bitboard:
            square = self.bsf(bitboard)

            if piece_type == "queen":
                attacks = (self.get_bishop_attacks(square) | self.get_rook_attacks(square)) & ~self.bitboards[color]
            elif piece_type == "bishop":
                attacks = self.get_bishop_attacks(square) & ~self.bitboards[color]
            elif piece_type == "rook":
                attacks = self.get_rook_attacks(square) & ~self.bitboards[color]
            elif piece_type == "king":
                attacks = self.attacks["king"][square] & ~self.bitboards[color]
                
                # Castling moves
                if self.castling != "-":
                    if color == "white":
                        if 'K' in self.castling and square == 4 and self.is_square_empty(5) and self.is_square_empty(6) and not self.is_attacking(4, "black") and not self.is_attacking(5, "black") and not self.is_attacking(6, "black"): # Check for kingside castling availability and if the squares are empty and not under attack
                            moves.append(encode_move(4, 6))  # Kingside castling
                        if 'Q' in self.castling and square == 4 and self.is_square_empty(3) and self.is_square_empty(2) and self.is_square_empty(1) and not self.is_attacking(4, "black") and not self.is_attacking(3, "black") and not self.is_attacking(2, "black"): # Check for queenside castling availability and if the squares are empty and not under attack
                            moves.append(encode_move(4, 2))  # Queenside castling
                    elif color == "black":
                        if 'k' in self.castling and square == 60 and self.is_square_empty(61) and self.is_square_empty(62) and not self.is_attacking(60, "white") and not self.is_attacking(61, "white") and not self.is_attacking(62, "white"): # Check for kingside castling availability and if the squares are empty and not under attack
                            moves.append(encode_move(60, 62))  # Kingside castling
                        if 'q' in self.castling and square == 60 and self.is_square_empty(59) and self.is_square_empty(58) and self.is_square_empty(57) and not self.is_attacking(60, "white") and not self.is_attacking(59, "white") and not self.is_attacking(58, "white"): # Check for queenside castling availability and if the squares are empty and not under attack
                            moves.append(encode_move(60, 58))  # Queenside castling
            elif piece_type == "knight":
                attacks = self.attacks["knight"][square] & ~self.bitboards[color]
            elif piece_type == "pawn":
                moves.extend(self.get_pawn_moves(square, color)) # Call dedicated pawn move function.
                bitboard &= ~(1 << square) #Move outside the loop since it can generate more than one move for the same piece.
                continue # Continue to the next piece, since the moves have already been added.
            else:
                raise ValueError(f"Unknown piece type: {piece_type}")

            while attacks:
                attack_square = self.bsf(attacks)
                moves.append(encode_move(square, attack_square))
                attacks &= ~(1 << attack_square)
            bitboard &= ~(1 << square)

        return moves

    def get_all_pseudo_legal_moves(self, color):
        moves = []
        for piece_type in ["king", "knight", "bishop", "rook", "queen", "pawn"]:  # Iterate through piece types
            moves.extend(self.generate_moves_for_piece(piece_type, color))
        return moves
    
    def get_all_valid_moves(self, color):
        all_pseudo_legal = self.get_all_pseudo_legal_moves(color)
        
        valid_moves = [move for move in all_pseudo_legal if self.validate_move(move, color)]

        return valid_moves
        
    def count_legal_moves(self, fen_string):
        """Counts the number of legal moves from a given FEN string.

        Args:
            fen_string: The FEN string representing the board position.

        Returns:
            The number of legal moves from that position.  Returns 0 if the FEN is invalid.
        """
        try:
            board = chess.Board(fen_string)
            return board.legal_moves.count()
        except ValueError: # handle invalid FEN
            return 0
        
    def get_bishop_attacks(self, square):
        all_pieces = self.get_all_pieces()
        blocker = all_pieces & self.masks["BISHOP"][square]
        magic_number, shift = BISHOP_MAGICS[square], BISHOP_SHIFTS[square]
        key = (blocker * magic_number) >> shift
        
        attacks = self.bishop_lookup[square][key]
        return attacks

    def get_rook_attacks(self, square):
        all_pieces = self.get_all_pieces()
        blocker = all_pieces & self.masks["ROOK"][square]
        magic_number, shift = ROOK_MAGICS[square], ROOK_SHIFTS[square]
        key = (blocker * magic_number) >> shift
        
        attacks = self.rook_lookup[square][key]
        return attacks
    
    def get_pawn_moves(self, square, color):
        moves = []
        rank = square // 8
        file = square % 8
        other_color = "white" if color == "black" else "black"
        direction = 8 if color == "white" else -8
        start_rank = 1 if color == "white" else 6

        # Single push
        target_square = square + direction
        rank_target_square = target_square // 8
        if self.is_square_empty(target_square):
            if rank_target_square == 7 or rank_target_square == 0: #Promotion check
                for promotion_piece in range(1, 5): #Promotion moves
                    moves.append(encode_move(square, target_square, promotion=promotion_piece)) #Add promotion move
            else:
                moves.append(encode_move(square, target_square))

            # Double push
            if rank == start_rank:
                target_square = square + 2 * direction
                if self.is_square_empty(target_square):
                    moves.append(encode_move(square, target_square))

        # Captures
        for capture_offset in [-1, 1]:
            target_file = file + capture_offset  # Calculate the target file
            if 0 <= target_file < 8:  # Check if the target file is inside the board
                target_square = square + direction + capture_offset
                if 0 <= target_square < 64:  # Check if it is on the board
                    if self.bitboards[other_color] & (1 << target_square) or target_square == self.en_passant:  # Check if it is a capture or en passant
                        target_rank = target_square // 8
                        if target_rank == 7 or target_rank == 0:  # Promotion check
                            for promotion_piece in range(1, 5):  # Promotion moves
                                moves.append(encode_move(square, target_square, promotion=promotion_piece))  # Add promotion move
                        else:
                            moves.append(encode_move(square, target_square))
        return moves
    
    def bsf(self, bitboard: int) -> int:
        return (bitboard & -bitboard).bit_length() - 1 if bitboard else -1

    def bsr(self, bitboard: int) -> int:
        return bitboard.bit_length() - 1 if bitboard else -1

    
    def get_all_pieces(self):
        return self.bitboards["white"] | self.bitboards["black"]
        
    def move_piece(self, bitboard_name: str, src: int, dst: int) -> int:
        # Clear the source square bit.
        self.remove_piece(bitboard_name, src)
        # Set the destination square bit.
        self.add_piece(bitboard_name, dst)
        self.update_color_bitboards()
        self.update_attack_bitboards()

    def remove_piece(self, bitboard_name: str, square: int) -> None:      
        self.bitboards[bitboard_name] &= ~(1 << square)
        self.update_color_bitboards()
        self.update_attack_bitboards()
    
    def add_piece(self, bitboard_name: str, square: int) -> None:
        self.bitboards[bitboard_name] |= (1 << square)
        self.update_color_bitboards()
        self.update_attack_bitboards()