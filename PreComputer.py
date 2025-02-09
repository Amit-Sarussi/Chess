import random

from chess import ROOK
from Constants import *

def generate_attacks():
    attacks = {}
    attacks["knight"] = generate_knight_attacks()
    attacks["king"] = generate_king_attacks()
    attacks["white_pawn_attacks"], attacks["black_pawn_attacks"] = generate_pawn_attacks()

    return attacks


def generate_knight_attacks():
    moves = {}
    for square in range(64):
        moves[square] = 0
        x = square % 8  # File (0-7)
        y = square // 8 # Rank (0-7)

        for dx, dy in [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1)]:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:  # Check board boundaries
                new_square = new_y * 8 + new_x
                moves[square] |= 1 << new_square
    return moves

def generate_king_attacks():
    moves = {}
    for square in range(64):
        moves[square] = 0
        x = square % 8
        y = square // 8

        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8: #Check board boundaries
                new_square = new_y * 8 + new_x
                moves[square] |= 1 << new_square
    return moves

def generate_pawn_attacks():
    white_attacks = {}
    black_attacks = {}

    for square in range(64):
        white_attacks[square] = 0
        black_attacks[square] = 0

        rank = square // 8
        file = square % 8

        # White pawn attacks
        if rank < 7:
            if file > 0:  # NW capture
                white_attacks[square] |= 1 << (square + 7)
            if file < 7:  # NE capture
                white_attacks[square] |= 1 << (square + 9)

        # Black pawn attacks
        if rank > 0:
            if file > 0:  # SW capture
                black_attacks[square] |= 1 << (square - 9)
            if file < 7:  # SE capture
                black_attacks[square] |= 1 << (square - 7)

    return white_attacks, black_attacks

def generate_masks():
    return {"ROOK": [create_rook_movement_mask(i) for i in range(64)], "BISHOP": [create_bishop_movement_mask(i) for i in range(64)]}

def generate_rays():
    rays = {}
    rays["NORTH"] = generate_rays_north()
    rays["NORTH_EAST"] = generate_rays_north_east()
    rays["EAST"] = generate_rays_east()
    rays["SOUTH_EAST"] = generate_rays_south_east()
    rays["SOUTH"] = generate_rays_south()
    rays["SOUTH_WEST"] = generate_rays_south_west()
    rays["WEST"] = generate_rays_west()
    rays["NORTH_WEST"] = generate_rays_north_west()
    return rays

def generate_rays_north():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while cell + 8 < 64:
            cell += 8
            rays[square] |= 1 << (cell)
    return rays

def generate_rays_north_east():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while (cell + 9) % 8 != 0 and cell + 9 < 64:
            cell += 9
            rays[square] |= 1 << (cell)
    return rays

def generate_rays_east():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while (cell + 1) % 8 != 0:
            cell += 1
            rays[square] |= 1 << (cell)
    return rays

def generate_rays_south_east():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while (cell -7) % 8 != 0 and cell - 7 >= 0:
            cell += -7
            rays[square] |= 1 << (cell)
    return rays

def generate_rays_south():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while cell - 8 >= 0:
            cell += -8
            rays[square] |= 1 << (cell)
    return rays

def generate_rays_south_west():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while (cell - 9) % 8 != 7 and cell - 9 >= 0:
            cell += -9
            rays[square] |= 1 << (cell)
    return rays

def generate_rays_west():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while (cell - 1) % 8 != 7:
            cell += -1
            rays[square] |= 1 << (cell)
    return rays

def generate_rays_north_west():
    rays = {-1: 0}
    for square in range(64):
        rays[square] = 0
        cell = square
        while (cell + 7) % 8 != 7 and cell + 7 < 64:
            cell += 7
            rays[square] |= 1 << (cell)
    return rays

def bsf(bitboard):
        # Bit Scan Forward: Find the first set bit (lowest 1-bit)
        if bitboard == 0:
            return -1  # No set bits
        return (bitboard & -bitboard).bit_length() - 1

def bsr(bitboard):
    # Bit Scan Reverse: Find the last set bit (highest 1-bit)
    if bitboard == 0:
        return -1  # No set bits
    return bitboard.bit_length() - 1

rays = generate_rays()

def create_rook_movement_mask(square):
    mask = 0
    
    north = rays["NORTH"][square]
    east = rays["EAST"][square]
    south = rays["SOUTH"][square]
    west = rays["WEST"][square]

    north_bsr = bsr(north)
    east_bsr = bsr(east)
    south_bsf = bsf(south)
    west_bsf = bsf(west)

    if north_bsr != -1:
        mask |= (north & ~(1 << north_bsr))
    if east_bsr != -1:
        mask |= (east & ~(1 << east_bsr))
    if south_bsf != -1:
        mask |= (south & ~(1 << south_bsf))
    if west_bsf != -1:
        mask |= (west & ~(1 << west_bsf))

    return mask

def create_bishop_movement_mask(square):
    mask = 0
    
    ne = rays["NORTH_EAST"][square]
    se = rays["SOUTH_EAST"][square]
    sw = rays["SOUTH_WEST"][square]
    nw = rays["NORTH_WEST"][square]

    ne_bsr = bsr(ne)
    se_bsf = bsf(se)
    sw_bsf = bsf(sw)
    nw_bsr = bsr(nw)

    if ne_bsr != -1:
        mask |= (ne & ~(1 << ne_bsr))
    if se_bsf != -1:
        mask |= (se & ~(1 << se_bsf))
    if sw_bsf != -1:
        mask |= (sw & ~(1 << sw_bsf))
    if nw_bsr != -1:
        mask |= (nw & ~(1 << nw_bsr))

    return mask

def get_rook_attacks(square, blockers):
    attacks = 0
    
    # North
    masked_blockers = blockers & rays["NORTH"][square]
    first_block = bsf(masked_blockers)
    attacks |= rays["NORTH"][square] & ~rays["NORTH"][first_block]
    
    # East
    masked_blockers = blockers & rays["EAST"][square]
    first_block = bsf(masked_blockers)
    attacks |= rays["EAST"][square] & ~rays["EAST"][first_block]
    
    # South
    masked_blockers = blockers & rays["SOUTH"][square]
    first_block = bsr(masked_blockers)
    attacks |= rays["SOUTH"][square] & ~rays["SOUTH"][first_block]
    
    # West
    masked_blockers = blockers & rays["WEST"][square]
    first_block = bsr(masked_blockers)
    attacks |= rays["WEST"][square] & ~rays["WEST"][first_block]
    
    return attacks

def get_bishop_attacks(square, blockers):      
    attacks = 0
        
    # North East
    masked_blockers = blockers & rays["NORTH_EAST"][square]
    first_block = bsf(masked_blockers)
    attacks |= rays["NORTH_EAST"][square] & ~rays["NORTH_EAST"][first_block]
    
    # South East
    masked_blockers = blockers & rays["SOUTH_EAST"][square]
    first_block = bsr(masked_blockers)
    attacks |= rays["SOUTH_EAST"][square] & ~rays["SOUTH_EAST"][first_block]
    
    # South West
    masked_blockers = blockers & rays["SOUTH_WEST"][square]
    first_block = bsr(masked_blockers)
    attacks |= rays["SOUTH_WEST"][square] & ~rays["SOUTH_WEST"][first_block]
    
    # North West
    masked_blockers = blockers & rays["NORTH_WEST"][square]
    first_block = bsf(masked_blockers)
    attacks |= rays["NORTH_WEST"][square] & ~rays["NORTH_WEST"][first_block]
    
    return attacks
      
def create_all_blocker_bitboards(movement_mask):
    square_indices = []
    for i in range(64):
        if ((movement_mask >> i) & 1) == 1:
            square_indices.append(i)
    
    num_patterns = 1 << len(square_indices) # 2^n
    blocker_bitboards = []
    for pattern_index in range(num_patterns):
        pattern = pattern_index
        bitboard = 0
        for i in range(len(square_indices)):
            if (pattern & 1) == 1:
                bitboard |= 1 << square_indices[i]
            pattern >>= 1
        blocker_bitboards.append(bitboard)
    return blocker_bitboards
    
def create_rook_lookup_table():
    """
    Create a lookup table for rook moves.
    The final structure is a dictionary mapping each square (0-63) to a sub-table.
    For a given square, the sub-table maps a magic index (computed from a blocker
    configuration) to the corresponding legal move bitboard.
    """
    rook_moves_lookup = {}
    for square in range(64):
        movement_mask = create_rook_movement_mask(square)
        blocker_patterns = create_all_blocker_bitboards(movement_mask)
        magic, shift = ROOK_MAGICS[square], ROOK_SHIFTS[square]
        lookup = {}  # sub-table for this square
        for blocker in blocker_patterns:
            # Compute the magic index from this blocker configuration.
            index = (blocker * magic) >> shift
            legal_move_bitboard = get_rook_attacks(square, blocker)
            # Store the legal moves for this blocker configuration at the computed index.
            lookup[index] = legal_move_bitboard
        # Save the sub-table for this square.
        rook_moves_lookup[square] = lookup
    return rook_moves_lookup

def create_bishop_lookup_table():
    bishop_moves_lookup = {}
    for square in range(64):
        movement_mask = create_bishop_movement_mask(square)
        blocker_patterns = create_all_blocker_bitboards(movement_mask)
        magic, shift = BISHOP_MAGICS[square], BISHOP_SHIFTS[square]
        lookup = {}  # sub-table for this square
        for blocker in blocker_patterns:
            # Compute the magic index from this blocker configuration.
            index = (blocker * magic) >> shift
            legal_move_bitboard = get_bishop_attacks(square, blocker)
            # Store the legal moves for this blocker configuration at the computed index.
            lookup[index] = legal_move_bitboard
        # Save the sub-table for this square.
        bishop_moves_lookup[square] = lookup
    return bishop_moves_lookup

def generate_magic_square(square, piece_type):
    if piece_type.upper() == "ROOK":
        movement_mask = create_rook_movement_mask(square)
        get_attacks = get_rook_attacks
    elif piece_type.upper() == "BISHOP":
        movement_mask = create_bishop_movement_mask(square)
        get_attacks = get_bishop_attacks
    else:
        raise ValueError("Unsupported piece type. Use 'ROOK' or 'BISHOP'.")
    
    # Count the number of relevant bits (r); these bits determine the size of the occupancy table.
    r = movement_mask.bit_count()
    shift = 64 - r  # We shift right by (64 - r) bits.

    # Generate all blocker occupancy configurations from the movement mask.
    blocker_occups = create_all_blocker_bitboards(movement_mask)

    # For each blocker occupancy, compute the corresponding (pre-calculated) attack bitboard.
    occupancy_to_attack = {}
    for occ in blocker_occups:
        occupancy_to_attack[occ] = get_attacks(square, occ)

    # Now search for a candidate magic number.
    while True:
        # To bias toward sparse candidates (which often work better), combine several random 64-bit numbers.
        candidate = random.getrandbits(64) & random.getrandbits(64) & random.getrandbits(64)
        used = {}  # mapping from computed index -> attack bitboard
        valid = True
        for occ in blocker_occups:
            # Compute the index using the candidate magic number.
            index = (occ * candidate) >> shift
            # If this index has already been used, it must map to the same attack bitboard.
            if index in used:
                if used[index] != occupancy_to_attack[occ]:
                    valid = False
                    break
            else:
                used[index] = occupancy_to_attack[occ]
        if valid:
            return candidate, shift

# def generate_magics():
#     rook_magics = {}
#     bishop_magics = {}
#     for square in range(64):
#         rook_magics[square] = generate_magic_square(square, "rook"), 
#         bishop_magics[square] = generate_magic_square(square, "bishop")
#     return rook_magics, bishop_magics


def print_bitboard(bitboard, reverse_rows=False):
    """Prints a 64-bit bitboard, optionally reversing rows vertically.

    Args:
        bitboard: The 64-bit integer representing the bitboard.
        reverse_rows: If True, reverses the order of rows when printing.
    """

    rows = []  # Store rows as strings
    for row in range(7, -1, -1):
        row_str = ""
        for col in range(8):
            index = row * 8 + col
            if (bitboard >> index) & 1:
                row_str += "1"
            else:
                row_str += "0"
        rows.append(row_str)

    if reverse_rows:
        rows = rows  # Reverse the list of rows

    for row_str in rows:
        print(row_str)