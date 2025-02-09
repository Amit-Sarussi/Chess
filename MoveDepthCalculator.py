from xml.etree.ElementPath import ops
import chess
from Board import Board, decode_move
from Constants import *


class MoveDepthCalculator():
    def __init__(self, depth):
        self.board = Board(STARTING_FEN)
        print(f"Counted: {self.start("white", depth)} moves for depth: {depth}")
    
    def start(self, turn, depth):
        if depth == 0:
            return 1  # Base case: count this position
        
        move_count = 0  # Define move_count *inside* the function
        all_moves = self.board.get_all_valid_moves(turn)  # Pass the turn to get_all_valid_moves

        for move in all_moves:
            
            self.board.make_move(move)
            
            
            switch_turn = "black" if turn == "white" else "white"
            move_in = self.start(switch_turn, depth - 1)  # Accumulate the results!
            move_count += move_in
            
            self.board.undo_move()

        return move_count