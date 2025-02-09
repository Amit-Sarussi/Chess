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


# def generate_pawn_moves():
#     white_moves = {}
#     black_moves = {}

#     for square in range(64):
#         white_moves[square] = 0
#         black_moves[square] = 0

#         rank = square // 8
#         file = square % 8

#         # White pawn moves
#         if rank < 7:
#             target_square = square + 8
#             white_moves[square] |= 1 << target_square  # Single push
#             if rank == 1:  # Double push
#                 white_moves[square] |= 1 << (square + 16)

#         # Black pawn moves
#         if rank > 0:
#             target_square = square - 8
#             black_moves[square] |= 1 << target_square  # Single push
#             if rank == 6:  # Double push
#                 black_moves[square] |= 1 << (square - 16)

#     return white_moves, black_moves

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