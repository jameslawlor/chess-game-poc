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
        self.double_move_active = False  # Track if double move is active

    def enable_double_move(self):
        """Enable the double move mechanic."""
        self.pending_second_move = True
        self.double_move_active = True

    def disable_double_move(self):
        """Disable the double move mechanic."""
        self.pending_second_move = False
        self.double_move_active = False


    # @property
    # def legal_moves(self):
    #     """Override legal_moves to allow the same player to move twice."""
    #     if self.double_move_active and self.pending_second_move:
    #         # Temporarily allow moves for the same color
    #         return self.generate_legal_moves(turn=self.turn)
    #     return super().legal_moves

    def push(self, move: chess.Move) -> None:
        """Push a move onto the board, handling double move logic."""
        if self.double_move_active and not self.pending_second_move:
            # Temporarily bypass turn enforcement for the second move
            self.turn = not self.turn
        super().push(move)
        # if self.pending_second_move:
        #     self.pending_second_move = False  # Consume the double move
        #     self.double_move_active = False  # Reset double move state