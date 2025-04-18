import chess.engine
import asyncio
from chess_game_poc.constants import STOCKFISH_PATH

class Engine:
    def __init__(self, path=STOCKFISH_PATH):
        self.path = path
        self.engine = None
        self.transport = None

    async def start(self):
        """Start the chess engine asynchronously."""
        self.transport, self.engine = await chess.engine.popen_uci(self.path)

    async def get_best_move(self, board: chess.Board, time_limit: float = 1.0) -> chess.Move:
        """Get the best move asynchronously."""
        if not self.engine:
            raise RuntimeError("Engine not started. Call `start()` first.")
        result = await self.engine.analyse(board, chess.engine.Limit(time=time_limit))
        return result["pv"][0]

    async def quit(self):
        """Quit the engine asynchronously."""
        if self.engine:
            await self.engine.quit()