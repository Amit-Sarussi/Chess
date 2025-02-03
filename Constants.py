from typing import Final

import Pawn, Rook, Knight, Bishop, Queen, King

# Graphics Settings
FRAME_RATE: Final = 165
SCREEN_SIZE: Final = (700, 700)
ICON: Final = "Assets/Icon.png"
CLOSE_ICON: Final = "Assets/close.png"
CHESS_COM_FONT = "Assets/ChessCom.ttf"
PIECES_DIR = "Assets/Pieces_Packs/Default/"
PIECE_SIZE = (SCREEN_SIZE[0] // (8), SCREEN_SIZE[1] // (8))
SHOW_FPS: Final = False
CLOSE_ICON_SIZE: Final = (20, 20)
CHECKMATE_ICON = "Assets/checkmate.png"
CHECKMATE_ICON_SIZE: Final = (28, 28)


# Sound Settings
FREQUENCY: Final = 44100
SIZE: Final = -16
CHANNELS: Final = 1 # Mono
BUFFER: Final = 512

# Board Settings
STARTING_FEN: Final = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
CHAR_TO_CLASS: Final = {
    'p': Pawn.Pawn,
    'r': Rook.Rook,
    'n': Knight.Knight,
    'b': Bishop.Bishop,
    'q': Queen.Queen,
    'k': King.King
}
LIGHT_SQUARE_COLOR: Final = (238, 238, 210)
DARK_SQUARE_COLOR: Final = (118, 150, 86)
SELECTED_SQUARE_COLOR = (255, 255, 51)
HOLD_INDICATOR_COLOR = (255, 255, 210)

GAME_DATA_DIR = "Games/"

