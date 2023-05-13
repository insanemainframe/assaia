import pytest

from game import GameState, GameExcpetion


@pytest.fixture
def game_state():
    return GameState()


def test_throw_x(game_state):
    with pytest.raises(GameExcpetion, match='invalid column'):
        game_state.make_throw(0, game_state.x)

    game_state.make_throw(0, game_state.x - 1)
    game_state.make_throw(1, 0)
    with pytest.raises(GameExcpetion, match='invalid column'):
        game_state.make_throw(0, -1)


def test_player_order(game_state):
    for i in range(6):
        game_state.make_throw(i % 2, 0)


def test_win_vertical(game_state):
    for i in range((game_state.win_condition - 1) * 2):
        player = i % 2
        game_state.make_throw(player, player)

    winner = game_state.make_throw(0, 0)
    assert winner == 0


def test_win_horizontal(game_state):
    col = 0
    for i in range((game_state.win_condition - 1) * 2):
        player = i % 2
        game_state.make_throw(player, col)
        col += player

    winner = game_state.make_throw(0, col)
    assert winner == 0


def test_win_diagonal(game_state):
    for i in range((game_state.win_condition - 1) * 2):
        player = i % 2
        game_state.make_throw(player, i)

    game_state.make_throw(0, i + 1)


def test_column_busy(game_state):
    with pytest.raises(GameExcpetion, match='column is busy'):
        for i in range(game_state.y * 2):
            player = i % 2
            game_state.make_throw(player, 0)
            print(game_state)
