import random
from Board import Board
from Player import Player
from Move import Move
class RandomPlayer(Player):
    def __init__(self, board: Board, color: str = 'w') -> None:
        super().__init__(board, color)

    def get_player_move(self) -> Move: 
        all_valid_moves = self.board.get_all_valid_moves(self.color)

        if len(all_valid_moves) == 0:
            return None
        return random.choice(all_valid_moves)