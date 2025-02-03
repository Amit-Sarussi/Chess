from datetime import datetime
import json
from Constants import *

def save_games_data(games_data):
    filename = str(len(games_data)) + "_" + datetime.now().strftime("%d.%m.%Y_%H%M") + ".json"
    file_dir = GAME_DATA_DIR + filename
    with open(file_dir, 'w') as f:
        json.dump(games_data, f)


