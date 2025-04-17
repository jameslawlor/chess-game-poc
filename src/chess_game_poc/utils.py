import chess

def print_board_pretty(board):
    print("  +---+---+---+---+---+---+---+---+")
    for rank in range(7, -1, -1):
        row = f"{rank + 1} |"
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            row += f" {piece.symbol() if piece else ' '} |"
        print(row)
        print("  +---+---+---+---+---+---+---+---+")
    print("    a   b   c   d   e   f   g   h  ")
