import pytest
import chess
from chess_game_poc.boards import CustomChessBoard

def test_switch_turn():
    board = CustomChessBoard()
    assert board.is_players_turn is True
    board.switch_turn()
    assert board.is_players_turn is False
    board.switch_turn()
    assert board.is_players_turn is True


def test_push_switches_turn():
    board = CustomChessBoard()
    move = chess.Move.from_uci("e2e4")
    board.push(move)
    assert board.is_players_turn is False


def test_teleport_rook_success():
    board = CustomChessBoard()
    board.set_piece_at(chess.parse_square("a1"), chess.Piece(chess.ROOK, chess.WHITE))
    board.teleport_rook("a1", "a3")
    assert board.piece_at(chess.parse_square("a1")) is None
    assert board.piece_at(chess.parse_square("a3")).piece_type == chess.ROOK


def test_teleport_rook_no_rook_at_source():
    board = CustomChessBoard()
    with pytest.raises(ValueError, match="Source square does not contain a rook."):
        board.teleport_rook("a2", "a3")


def test_teleport_rook_target_occupied():
    board = CustomChessBoard()
    board.set_piece_at(chess.parse_square("a1"), chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(chess.parse_square("a3"), chess.Piece(chess.PAWN, chess.WHITE))
    with pytest.raises(ValueError, match="Target square is already occupied."):
        board.teleport_rook("a1", "a3")