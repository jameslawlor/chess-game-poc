import asyncio
import chess
from chess_game_poc.engine import Engine
from chess_game_poc.boards import CustomChessBoard
from chess_game_poc.utils import print_board_pretty, display_welcome_message
from chess_game_poc.constants import MAX_ENGINE_ELO


async def get_engine_move(board):
    tmp_engine = Engine()
    await tmp_engine.start(MAX_ENGINE_ELO)
    move = await tmp_engine.get_move(board)
    print("\nEngine suggests the move:", move)
    await tmp_engine.quit()


async def handle_player_move(board, move_input):
    if move_input.lower() == "get_engine_move":
        print("Getting engine move...")
        await get_engine_move(board)
    elif move_input.lower() == "teleport":
        print("Teleport move activated!")
        source_square = input("Enter the source square (e.g., a1): ").strip()
        target_square = input("Enter the target square (e.g., d4): ").strip()
        try:
            board.teleport_rook(source_square, target_square)
            print_board_pretty(board)
        except ValueError as e:
            print(f"Error: {e}")

    else:
        try:
            move = chess.Move.from_uci(move_input)

            if move not in board.legal_moves:
                raise ValueError("Illegal move.")

            board.push(move)
            print_board_pretty(board)

        except ValueError as e:
            print(f"Invalid move: {e}")


async def handle_computer_move(engine, board):
    print("\nComputer is thinking...")
    computer_move = await engine.get_move(board)
    board.push(computer_move)
    print("\nComputer's move:", computer_move)
    print_board_pretty(board)


async def play_game():

    board = CustomChessBoard()
    engine = Engine()

    display_welcome_message()
    print_board_pretty(board)

    await engine.start()
    await engine.set_difficulty_with_player_input()

    try:
        while not board.is_game_over():
            if board.is_players_turn:
                move_input = input("\nYour move: ").strip()

                if move_input.lower() == "quit":
                    print("Thanks for playing!")
                    break

                await handle_player_move(board, move_input)

            else:
                # Computer's turn
                await handle_computer_move(engine, board)

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
