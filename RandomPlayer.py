import random
from Board import Board
from Player import Player

class RandomPlayer(Player):
    def __init__(self, board: Board, color: str = 'w') -> None:
        super().__init__(board, color)

    def get_player_move(self):
        # Get all possible moves
        possible_moves = self.board.get_possible_moves(self.color)

        # Remove the one that leaves the king in check
        possible_moves = [move for move in possible_moves if not self.board.move_puts_king_in_check(*move, self.color)]

        if len(possible_moves) == 0:
            return None
        return random.choice(possible_moves)