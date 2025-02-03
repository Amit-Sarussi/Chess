from Board import Board
from Constants import *

class PositionCounter:
    def __init__(self, depth=1):
        self.starting_board = Board(FEN_board=STARTING_FEN, color='w')
        self.starting_depth = depth
        counts = self.count_positions(self.starting_board, self.starting_depth)
        print(f"Position Count for depth: {depth} is: {counts}")
    
    def count_positions(self, board: Board, depth):
        if depth == 0: 
            return 1

        counter = 0
        possible_moves = board.get_all_valid_moves(board.turn)
        for move in possible_moves:
            board.make_move(move)
            counter += self.count_positions(board, depth=depth-1)
            board.undo_move(move)
        
        return counter
            


