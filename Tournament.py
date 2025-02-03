from Controller import Controller
from PlayerTypes import PlayerType
from GameDataSaver import save_games_data

class Tournament:
    def __init__(self, Player1Type, Player2Type, num_games = 1, save_results = True):
        self.controller = Controller(player1=Player1Type, player2=Player2Type)
        self.num_games = num_games
        self.save_results = save_results
        self.games_data = []
                
    def start(self):
        for i in range(self.num_games):
            result = self.controller.start()
            self.games_data.append(result["game_data"])
            
            if (i + 1) % 10 == 0:
                print(f"Finished game {i + 1} out of {self.num_games}")
                
        if self.save_results:
            save_games_data(games_data=self.games_data)
        