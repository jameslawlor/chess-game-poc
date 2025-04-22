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


def display_welcome_message():
    """Display the welcome message and available powers."""
    print("Welcome to James' Chess Game!")
    print("Enter your moves in SAN notation (e.g., 'e2e4'). Type 'quit' to exit.\n")
