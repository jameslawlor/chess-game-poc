import chess

# --- Setup board with custom position (all pawns = rooks) ---
# board = chess.Board(None)  # Empty board
# board = CustomChessBoard()

# # White rooks on rank 2 (normally pawns)
# for file in range(8):
#     board.set_piece_at(chess.square(file, 1), chess.Piece(chess.ROOK, chess.WHITE))
# Add kings so Stockfish is happy
# board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
# board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))

class CustomChessBoard(chess.Board):
    def __init__(self, fen=chess.STARTING_FEN, chess960=False):
        super().__init__(fen=fen, chess960=chess960)
        self.rook_teleport_available = True
        self.pending_second_move = False

    def is_legal(self, move: chess.Move) -> bool:
        # Allow standard legal moves
        if super().is_legal(move):
            return True

        # Allow a one-time rook teleport (any rook to any empty square)
        if self.rook_teleport_available:
            piece = self.piece_at(move.from_square)
            if piece and piece.piece_type == chess.ROOK and self.is_empty(move.to_square):
                return True

        return False

    def push(self, move: chess.Move) -> None:
        # If this is a rook teleport move, consume the power
        if not super().is_legal(move):
            piece = self.piece_at(move.from_square)
            if self.rook_teleport_available and piece and piece.piece_type == chess.ROOK:
                self.rook_teleport_available = False
        super().push(move)

    def is_empty(self, square: chess.Square) -> bool:
        return self.piece_at(square) is None