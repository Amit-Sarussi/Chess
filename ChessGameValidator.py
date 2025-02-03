import os
import json
import chess

class ChessGameValidator:
    def __init__(self, games_folder="Games"):
        self.games_folder = games_folder
        self.invalid_games = {}
        self.validate_all_games()

    def validate_game(self, game_data):
        """Validates a single game file and returns a list of invalid moves."""

        board = chess.Board(game_data["starting_fen"])
        invalid_moves = []

        for move_str in game_data["data"]:
            move = chess.Move.from_uci(move_str)
            if move in board.legal_moves:
                board.push(move)
            else:
                invalid_moves.append(move_str)

        return invalid_moves

    def validate_all_games(self):
        """Iterates through all JSON files in the folder and validates them."""
        if not os.path.exists(self.games_folder):
            print(f"Folder '{self.games_folder}' not found.")
            return

        for filename in os.listdir(self.games_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(self.games_folder, filename)
                with open(file_path, "r") as f:
                    games_data = json.load(f)
                
                for game in games_data:        
                    invalid_moves = self.validate_game(game)

                    if invalid_moves:
                        print(game)
                        self.invalid_games[filename + "_" + str(games_data.index(game))] = invalid_moves

        self.print_summary()

    def print_summary(self):
        """Prints a summary of invalid moves for all checked games."""
        if not self.invalid_games:
            print("✅ All games are valid!")
        else:
            print("❌ Invalid moves found in the following games:")
            for game, moves in self.invalid_games.items():
                print(f"  - {game}: {moves}")

