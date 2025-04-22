import pytest
import chess
from chess_game_poc.engine import Engine
from unittest.mock import AsyncMock, patch
import re 

@pytest.mark.asyncio
async def test_start_engine():
    with patch("chess.engine.popen_uci", new_callable=AsyncMock) as mock_popen_uci:
        mock_transport = AsyncMock()
        mock_engine = AsyncMock()
        mock_popen_uci.return_value = (mock_transport, mock_engine)

        engine = Engine(path="mock_path")
        await engine.start(elo=1500)

        mock_popen_uci.assert_called_once_with("mock_path")
        assert engine.transport == mock_transport
        assert engine.engine == mock_engine
        mock_engine.configure.assert_called_once_with(
            {"UCI_LimitStrength": True, "UCI_Elo": 1500}
        )


@pytest.mark.asyncio
async def test_set_difficulty():
    mock_engine = AsyncMock()
    engine = Engine()
    engine.engine = mock_engine

    await engine.set_difficulty(elo=1800)

    assert engine.elo == 1800
    assert engine.limit_strength is True
    mock_engine.configure.assert_called_once_with(
        {"UCI_LimitStrength": True, "UCI_Elo": 1800}
    )


@pytest.mark.asyncio
async def test_get_move():
    mock_engine = AsyncMock()
    mock_engine.analyse.return_value = {"pv": [chess.Move.from_uci("e2e4")]}
    engine = Engine()
    engine.engine = mock_engine

    board = chess.Board()
    move = await engine.get_move(board, time_limit=1.0)

    assert move == chess.Move.from_uci("e2e4")
    mock_engine.analyse.assert_called_once_with(
        board, chess.engine.Limit(time=1.0)
    )


@pytest.mark.asyncio
async def test_get_move_engine_not_started():
    engine = Engine()

    with pytest.raises(RuntimeError, match=re.escape("Engine not started. Call `start()` first.")):
        board = chess.Board()
        await engine.get_move(board)


@pytest.mark.asyncio
async def test_quit_engine():
    mock_engine = AsyncMock()
    engine = Engine()
    engine.engine = mock_engine

    await engine.quit()

    mock_engine.quit.assert_called_once()