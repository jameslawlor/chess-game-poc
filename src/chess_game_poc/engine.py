import chess.engine
import asyncio
from chess_game_poc.constants import STOCKFISH_PATH


class Engine:
    def __init__(self, path=STOCKFISH_PATH):
        self.path = path
        self.engine = None
        self.transport = None
        self.limit_strength = False
        self.elo = None

    async def start(self):
        """Start the chess engine asynchronously."""
        self.transport, self.engine = await chess.engine.popen_uci(self.path)

        input_difficulty = input("\nSet difficulty (ELO): ").strip()
        if (
            not input_difficulty
            or int(input_difficulty) < 1320
            or int(input_difficulty) > 3190
        ):
            print("Invalid ELO. Setting to default (1600).")
            input_difficulty = "1600"
        await self.set_difficulty(int(input_difficulty))

    async def set_difficulty(self, elo: int):
        """Set the difficulty of the engine."""
        self.elo = elo
        self.limit_strength = True
        await self.engine.configure(
            {
                "UCI_LimitStrength": self.limit_strength,
                "UCI_Elo": self.elo,
            }
        )

    async def _show_settings(self):
        print(dict(self.engine.protocol.config))

    async def get_move(self, board: chess.Board, time_limit: float = 1.0) -> chess.Move:
        """Get the move asynchronously."""
        if not self.engine:
            raise RuntimeError("Engine not started. Call `start()` first.")
        result = await self.engine.analyse(
            board,
            chess.engine.Limit(time=time_limit),
        )
        return result["pv"][0]

    async def quit(self):
        """Quit the engine asynchronously."""
        if self.engine:
            await self.engine.quit()
