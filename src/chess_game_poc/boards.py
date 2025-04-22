import chess


class CustomChessBoard(chess.Board):
    def __init__(self, fen=chess.STARTING_FEN, chess960=False):
        super().__init__(fen=fen, chess960=chess960)
        self.is_players_turn = True
        self.rook_teleport_available = True
        self.double_move_active = False
        self.pending_second_move = False

    def switch_turn(self):
        """Switch the turn between the player and the opponent."""
        self.is_players_turn = not self.is_players_turn

    def push(self, move: chess.Move) -> None:
        """
        Push a move onto the board.
        """
        super().push(move)
        self.switch_turn()
