from Controller import Controller
from Constants import *
from GameViewer import GameViewer
from PlayerTypes import PlayerType
from PositionCounter import PositionCounter
from ChessGameValidator import ChessGameValidator
import time
from Tests import *
from Tournament import Tournament

tournament = Tournament(Player1Type=PlayerType.RandomPlayer, Player2Type=PlayerType.RandomPlayer, num_games=1000, save_results=True)
tournament.start()

# controller = Controller(player1=PlayerType.RandomPlayer, player2=PlayerType.RandomPlayer)
# result = controller.start()
# winner = result["result"]
# game_data = result["game_data"]

# print(winner)
# print(controller.get_board())
# save_game_data(game_data=game_data)

#game_viewer = GameViewer(filename="20250129_103106", time_between=100)

# tic = time.time()
# position_counter = PositionCounter(depth=4)
# toc = time.time()
# print(f"Time Taken: {toc-tic}")

chessGameValidator = ChessGameValidator()