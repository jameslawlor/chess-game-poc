import chess


class CustomChessBoard(chess.Board):
    def __init__(self, fen=chess.STARTING_FEN, chess960=False):
        super().__init__(fen=fen, chess960=chess960)
        self.is_players_turn = True

    def switch_turn(self):
        """Switch the turn between the player and the opponent."""
        self.is_players_turn = not self.is_players_turn

    def push(self, move: chess.Move) -> None:
        """
        Push a move onto the board.
        """
        super().push(move)
        self.switch_turn()

    def teleport_rook(
        self,
        source_square: chess.Square,
        target_square: chess.Square,
    ) -> None:
        """
        Teleport a rook from source_square to target_square.
        """
        source_square_parsed = chess.parse_square(source_square)
        target_square_parsed = chess.parse_square(target_square)
        if not self.piece_type_at(source_square_parsed) == chess.ROOK:
            raise ValueError("Source square does not contain a rook.")
        if self.piece_type_at(target_square_parsed) is not None:
            raise ValueError("Target square is already occupied.")
        piece = self.piece_at(source_square_parsed)
        self.remove_piece_at(source_square_parsed)
        self.set_piece_at(target_square_parsed, piece)

        self.push(
            chess.Move.null()
        )  # trick the engine into thinking a normal move was made
