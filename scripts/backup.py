import chess
import chess.engine
from chess_game_poc.utils import print_board_pretty


stockfish_path = "/opt/homebrew/bin/stockfish"
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
board = chess.Board()
board.remove_piece_at(chess.A2)
board.set_piece_at(chess.A2, chess.Piece(chess.PAWN, chess.WHITE))
print("Starting state:")
print_board_pretty(board)

custom_move = chess.Move.from_uci("a2a5")
print(board.is_legal(custom_move))
board.push(custom_move)
print_board_pretty(board)
# board.remove_piece_at(chess.A2)
# board.set_piece_at(chess.A2, chess.Piece(chess.PAWN, chess.WHITE))
board.clear_stack()
# stop

# Do some illegal move
# board.remove_piece_at(chess.A2)
# board.set_piece_at(chess.A2, chess.Piece(chess.PAWN, chess.WHITE))
# board.turn = chess.BLACK
# print_board_pretty(board)
# engine.analysis()
print("Stockfish will now move...")
result = engine.analyse(board, chess.engine.Limit(time=1.0))
print(result)
board.push(result["pv"][0])
print_board_pretty(board)

while not board.is_game_over():
    print_board_pretty(board)

    try:
        move_str = input("Your move: ")
        move = chess.Move.from_uci(move_str)
        if not board.is_legal(move):
            print("Illegal move......")
            raise ValueError
        # board.push_san(move)
        else:
            board.push(move)
    except ValueError as e:
        print("Invalid move. Try again.")
        print(f"Error: {e}")
        continue

    print_board_pretty(board)
    result = engine.analyse(board, chess.engine.Limit(time=1.0))
    move = result["pv"][0]
    print(f"Stockfish plays: {board.san(move)}")
    board.push(move)

engine.quit()
