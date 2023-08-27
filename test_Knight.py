from typing import List, Tuple
from unittest.mock import Mock

from enums import Player
from Piece import Knight


def get_game_state_mock(player: Player, occupied_points: List[Tuple[int, int]]):
    """
    Creates a mock of the game_state class
    :param player: The other player
    :param occupied_points: A list of points that are occupied by the other player
    :return: A mock of the game_state class
    """
    def get_piece_mock(row: int, col: int):
        if row in range(8) and col in range(8):
            return player if (row, col) in occupied_points else Player.EMPTY
        else:
            return None

    game_state_mock = Mock()
    game_state_mock.get_piece.side_effect = get_piece_mock
    return game_state_mock


def test_get_valid_peaceful_moves():
    """
    Tests the get_valid_peaceful_moves method of the Knight class in case of that the knight in the middle of the board
    and there are not any occupied squares
    """
    knight = Knight('n', 3, 5, Player.PLAYER_1)
    game_state_mock = get_game_state_mock(Player.PLAYER_2, [])
    assert set(knight.get_valid_peaceful_moves(game_state_mock)) == {(2, 3), (1, 4), (1, 6), (2, 7), (4, 7), (5, 6),
                                                                     (5, 4), (4, 3)}


def test_get_valid_peaceful_moves_knight_at_corner():
    """
    Tests the get_valid_peaceful_moves method of the Knight class in case of that the knight at the corner of the board
    and there are not any occupied squares
    """
    knight = Knight('n', 0, 0, Player.PLAYER_1)
    game_state_mock = get_game_state_mock(Player.PLAYER_2, [])
    assert set(knight.get_valid_peaceful_moves(game_state_mock)) == {(1, 2), (2, 1)}


def test_get_valid_peaceful_moves_with_occupied_squares():
    """
    Tests the get_valid_peaceful_moves method of the Knight class in case of that the knight in the middle of the board
    and there are some occupied squares
    """
    knight = Knight('n', 3, 5, Player.PLAYER_1)
    game_state_mock = get_game_state_mock(Player.PLAYER_2, [(2, 3), (1, 4), (1, 6), (2, 7), (4, 7), (5, 6)])
    assert set(knight.get_valid_peaceful_moves(game_state_mock)) == {(5, 4), (4, 3)}
