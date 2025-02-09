from MoveDepthCalculator import MoveDepthCalculator
import time

tic = time.perf_counter()
MoveDepthCalculator(depth=3)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

tic = time.perf_counter()
MoveDepthCalculator(depth=4)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

# from Board import Board

# fen = "5k2/5P1p/2BP1P2/4q1p1/3P4/2K1p2p/1p3rPb/8 w - - 0 1"
# board = Board(fen)
# print(len(board.get_all_valid_moves(board.turn)))
# print(board.count_legal_moves(fen))
