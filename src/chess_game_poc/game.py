import asyncio
import chess
from chess_game_poc.engine import Engine
from chess_game_poc.player import Player
from chess_game_poc.custom_boards import CustomChessBoard
from chess_game_poc.powers import DoubleMovePower, RookTeleportPower
from chess_game_poc.utils import print_board_pretty


def display_welcome_message(player):
    """Display the welcome message and available powers."""
    print("Welcome to James' Chess Game!")
    print("Enter your moves in SAN notation (e.g., 'e2e4'). Type 'quit' to exit.\n")
    print("Available powers:")
    for power in player.powers:
        print(f"- {power.name}: {power.description}")
    print("\nYou can activate a power by typing 'power <power_name>' (e.g., 'power Double Move').")
    print("Note: Powers can only be used once per game.\n")


def handle_power_activation(player, board, power_name):
    """Handle the activation of a power."""
    if player.use_power(power_name):
        if power_name == "Double Move":
            board.enable_double_move()
            print(f"Power '{power_name}' activated!")
        elif power_name == "Rook Teleport":
            print(f"Power '{power_name}' activated! (Rook teleport logic not implemented yet.)")
    else:
        print(f"Power '{power_name}' is not available or does not exist.")


def handle_player_move(board, move_input):
    """Handle the player's move."""
    try:
        move = chess.Move.from_uci(move_input)
        if move not in board.legal_moves:
            raise ValueError("Illegal move.")
        board.push(move)
        print("\nYour move:", move_input)
        print_board_pretty(board)
        return True
    except ValueError as e:
        print(f"Invalid move: {e}")
        return False


def handle_second_move(board):
    """Handle the player's second move when Double Move is active."""
    print("Double Move activated! Make your second move.")
    second_move_input = input("\nYour second move: ").strip()
    board.push(chess.Move.null()) # pass the computer's turn
    if handle_player_move(board, second_move_input):
        board.disable_double_move()  # Disable the double move after use
        return True
    return False


async def handle_computer_move(engine, board):
    """Handle the computer's move."""
    print("\nComputer is thinking...")
    best_move = await engine.get_best_move(board)
    board.push(best_move)
    print("\nComputer's move:", best_move)
    print_board_pretty(board)


async def play_game():
    # Initialize the board, player, and engine
    board = CustomChessBoard()
    player = Player()
    engine = Engine()

    # Add powers to the player
    player.add_power(DoubleMovePower())
    player.add_power(RookTeleportPower())

    # Display welcome message and initial board
    display_welcome_message(player)
    print_board_pretty(board)

    # Start the chess engine
    await engine.start()

    try:
        while not board.is_game_over():
            
            # Player's turn
            move_input = input("\nYour move: ").strip()
            if move_input.lower() == "quit":
                print("Thanks for playing!")
                break

            if move_input.startswith("power "):
                # Handle power activation
                power_name = move_input.split(" ", 1)[1]
                handle_power_activation(player, board, power_name)
                continue

            if handle_player_move(board, move_input):
                # Handle second move if Double Move is active
                if board.pending_second_move:
                    if not handle_second_move(board):
                        continue

                # Check if the game is over after the player's move(s)
                if board.is_game_over():
                    print("\nGame over!")
                    print("Result:", board.result())
                    break

                # Computer's turn
                await handle_computer_move(engine, board)

                # Check if the game is over after the computer's move
                if board.is_game_over():
                    print("\nGame over!")
                    print("Result:", board.result())
                    break

    finally:
        # Quit the engine when the game ends
        await engine.quit()


# Run the game
if __name__ == "__main__":
    asyncio.run(play_game())