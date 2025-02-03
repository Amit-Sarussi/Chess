import chess
from Board import Board
from Move import Move
from Constants import *

def test_notation_to_move():
    board = Board(STARTING_FEN)
    notation = "e2e4"
    move = move.notation_to_move(notation)
    print(move.get())

def test_undo_move():
    board = Board(STARTING_FEN)
    move = Move((6, 4), (4, 4))  # e2 to e4
    before = board.board_to_FEN()
    print("Before move:", before)
    board.make_move(move)
    print("After move:", board.board_to_FEN())  # Check state after move

    board.undo_move(move)
    print("After undo:", board.board_to_FEN())  # Check state after undo
    
    if board.board_to_FEN() == before:
        print("Test passed")
    else:
        print("Test failed")

def test_piece():
    board = Board(STARTING_FEN)
    print(board.board[7,7])

def test_promote_fail():
    board = Board("k7/4P1R1/5Q1N/8/8/8/PPPPK2P/RNB5 w - - 17 37")
    for m in board.board[1,4].get_pseudo_legal_moves(board): print(m)
    print(board.validate_move(Move((1, 4), (0, 4), promotion="q"), "w", check_pseudo_legal=True, log=True))

def check_castle_while_under_attack():
    board: Board = Board(FEN_board="1n2qb1r/1p1kPp1p/r6P/p1pp1b2/8/8/PPPPP3/RNBQKBN1 w Q - 1 12", color='w')
    move = Move((6, 1), (0, 2), promotion='q')
    print(board.validate_move(move, 'w', check_pseudo_legal=True))

def check_why_error():
    board: Board = Board(FEN_board="r3k2r/ppP2pp1/5n2/3p3p/2QNP2P/bPNB3b/n2P2P1/3RK1R1 b q - 3 23", color='w')
    move = Move((0, 4), (0, 2))

def check_why_error_2():
    game_data = {'starting_fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'data': ['b2b3', 'c7c6', 'c2c4', 'g8f6', 'a2a3', 'e7e5', 'f2f4', 'h8g8', 'b1c3', 'd8b6', 'g1f3', 'f8b4', 'c3a4', 'b8a6', 'h2h4', 'g8h8', 'e2e4', 'h7h5', 'f4e5', 'f6d5', 'e5e6', 'b4c3', 'c1b2', 'b6b5', 'h1g1', 'h8h7', 'c4b5', 'a6b4', 'd1e2', 'd5f6', 'a1d1', 'd7d5', 'b5c6', 'c3b2', 'e2b5', 'b4a2', 'b5c4', 'h7h8', 'f1d3', 'b2a3', 'c6c7', 'c8e6', 'f3d4', 'e6h3', 'a4c3', 'e8c8', 'd3c2', 'f6e4', 'c4d5', 'e4g3', 'c2f5', 'g3f5', 'g2g3', 'a3d6', 'd5f7', 'h8g8', 'd4c6', 'b7c6', 'c3b5', 'd6b4', 'd1c1', 'c8b7', 'c7d8n', 'b7c8', 'f7a7', 'g8e8', 'a7e3', 'f5d6', 'd8c6', 'b4a5', 'b5c7', 'e8e4', 'c6a7', 'c8d8', 'c1c3', 'a5b4', 'g3g4', 'e4e7', 'c3c2', 'd6b7', 'c7d5', 'e7e4', 'g1g3', 'b7a5', 'd5e7', 'e4c4', 'a7c6', 'c4c6', 'g4h5', 'g7g6', 'c2c4', 'h3c8', 'g3f3', 'g6g5', 'e3c3', 'a2c1', 'c4c5', 'c8d7', 'c3g7', 'c6c8', 'e7f5', 'b4c3', 'g7f7', 'c8b8', 'f3g3', 'a5b3', 'g3c3', 'b3a5', 'c5a5', 'c1d3', 'e1e2', 'd3f2', 'c3a3', 'g5g4', 'f7e8', 'd7e8', 'f5g3', 'b8b1', 'a5d5', 'd8c8', 'a3a1', 'b1c1', 'a1a2', 'c1f1', 'a2a5', 'e8a4', 'a5a6', 'a4b3', 'd2d4', 'c8c7', 'a6c6', 'c7b8', 'c6c7', 'f2d1', 'c7c4', 'd1b2', 'c4c3', 'f1f3', 'd5c5', 'b8a8', 'c3c2', 'a8b7', 'c5a5', 'b3e6', 'c2c7', 'b7c7', 'a5a7', 'c7d8', 'a7a8', 'd8e7', 'a8a3', 'e6f7', 'a3a1', 'f7c4', 'e2d2', 'e7f7', 'g3h1', 'f7e7', 'a1a8', 'c4e6', 'd2e1', 'e6d7', 'a8a7', 'f3c3', 'h1f2', 'b2d1', 'a7a3', 'd7c6', 'e1f1', 'c3h3', 'a3b3', 'c6b5', 'b3b5', 'e7f7', 'f2h1', 'h3h1', 'f1e2', 'd1b2', 'd4d5', 'f7g7', 'b5c5', 'h1c1', 'c5a5', 'c1a1', 'a5a7', 'a1a7', 'e2e1', 'b2c4', 'e1d1', 'a7a2', 'h5h6', 'g7g6', 'd1c1', 'a2a3', 'h6h7', 'g6f6', 'h7h8q', 'f6g6', 'h8e8', 'g6f5', 'e8c8', 'f5e4', 'c8e8', 'e4d5', 'e8e3', 'c4d2', 'e3e1', 'a3a1', 'c1c2', 'd2b1', 'e1f2', 'd5e6', 'h4h5', 'a1a5', 'f2f6', 'e6f6', 'c2b3', 'a5c5', 'b3b4', 'f6f7', 'b4c5', 'g4g3', 'c5c4', 'b1d2', 'c4b4', 'f7f8', 'b4a5', 'f8g8', 'a5b5', 'd2b1', 'h5h6', 'g8h8', 'b5a4', 'h8h7', 'a4b5', 'h7h8', 'b5b6', 'h8g8', 'b6a6', 'g8f7', 'a6b5', 'f7f8', 'b5c5', 'b1c3', 'h6h7', 'c3b5', 'h7h8q', 'f8e7', 'h8h5', 'b5a3', 'h5d5', 'a3c2', 'd5d2', 'c2d4', 'd2b4', 'd4c2', 'b4d4', 'c2d4', 'c5b6', 'g3g2', 'b6a6', 'g2g1r', 'a6a5', 'g1g2', 'a5a4', 'e7e6', 'a4a3', 'd4f5', 'a3a4', 'f5h6', 'a4a3', 'g2g4', 'a3b2', 'e6f5', 'b2b1', 'g4g7', 'b1b2', 'f5e5', 'b2c1', 'e5d5', 'c1b2', 'd5d6', 'b2c1', 'd6d7', 'c1d2', 'g7f7', 'd2c2', 'h6g8', 'c2d3', 'f7f8', 'd3d2', 'f8f3', 'd2e1', 'f3f2', 'e1f2', 'g8h6', 'f2g2', 'h6f7', 'g2f3', 'f7d6', 'f3e2', 'd6c4', 'e2d3', 'd7e6', 'd3e2', 'e6f6', 'e2d3', 'f6g7', 'd3c2', 'g7h8', 'c2d3', 'c4a5', 'd3e3', 'a5c4', 'e3d4', 'c4e5', 'd4e4', 'e5g6', 'e4f3', 'h8h7', 'f3g4', 'g6e7', 'g4f3', 'h7g6', 'f3f4', 'e7g8', 'f4g3', 'g6g5', 'g3h2', 'g5f6', 'h2g2', 'g8h6', 'g2f2', 'f6g6', 'f2g2', 'g6h5', 'g2h2', 'h5g6', 'h2h3', 'h6g4', 'h3g2', 'g6h6', 'g2h1', 'g4f2', 'h1h2', 'f2e4'], 'result': 't'}
    print(validate_game(game_data))
    
def validate_game(game_data):
        """Validates a single game file and returns a list of invalid moves."""

        board = chess.Board(game_data["starting_fen"])
        invalid_moves = []

        for move_str in game_data["data"]:
            move = chess.Move.from_uci(move_str)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Fen now:", board.fen())
                print("Invalid move:", move_str)
                
                invalid_moves.append(move_str)

        return invalid_moves
    
if __name__ == "__main__":
    check_why_error()