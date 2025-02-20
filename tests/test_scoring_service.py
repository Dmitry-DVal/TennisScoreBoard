from contextlib import nullcontext as does_not_raise

import pytest

from src.services.scoring_service import Match, Set, Game


class TestMatchScoring:

    @pytest.mark.parametrize(
        "games, player, result, is_tie_break, expectation",
        [
            ([4, 5], 1, [4, 6], False, does_not_raise()),
            ([5, 5], 1, [5, 6], False, does_not_raise()),
            ([5, 6], 0, [6, 6], True, does_not_raise()),
            ([5, 6], 1, [5, 7], False, does_not_raise()),
            ([0, 0], 0, [1, 0], False, does_not_raise()),
            ([1, 0], 1, [1, 1], False, does_not_raise()),
            ([2, 0], 0, [3, 0], False, does_not_raise()),
            ([0, 1], "1", [0, 1], False, pytest.raises(TypeError)),
            ([0, 1], [1], [0, 1], False, pytest.raises(TypeError)),
            ([0, 1], {1}, [0, 1], False, pytest.raises(TypeError)),
            ([0, 1], 2, [0, 1], False, pytest.raises(IndexError)),
        ]
    )
    def test_set_add_game(self, games, player, result, is_tie_break, expectation):
        "Правильность добавления геймов в сете."
        set1 = Set(Match())
        set1.games = games
        with expectation:
            set1.add_game(player)
            assert set1.games == result
            assert set1.is_tie_break == is_tie_break

    @pytest.mark.parametrize(
        "scores, player, result, expectation",
        [
            ([40, 40], 1, [40, 'ad'], does_not_raise()),
            ([40, 40], 0, ['ad', 40], does_not_raise()),
            ([15, 40], 1, [15, 60], does_not_raise()),
            ([40, 'ad'], 1, [40, 60], does_not_raise()),
            (['ad', 40], 1, [40, 40], does_not_raise()),
            (['ad', 40], 0, [60, 40], does_not_raise()),
            ([0, 0], 0, [15, 0], does_not_raise()),
            ([15, 0], 0, [30, 0], does_not_raise()),
            ([30, 0], 0, [40, 0], does_not_raise()),
            ([40, 0], 0, [60, 0], does_not_raise()),
            ([0, 15], "1", [0, 15], pytest.raises(TypeError)),
            ([0, 15], [1], [0, 15], pytest.raises(TypeError)),
            ([0, 15], {1}, [0, 15], pytest.raises(TypeError)),
            ([0, 15], 2, [0, 15], pytest.raises(IndexError)),
        ]
    )
    # Обработчка передачи других типов данных. ? Если это вообще надо.
    def test_game_add_point(self, scores, player, result, expectation):
        "Правильность добавления очков при стандартном гейме."
        game = Game(Set(Match()))
        game.scores = scores
        with expectation:
            game.add_point(player)
            assert game.scores == result

    @pytest.mark.parametrize(
        "scores, player, result, expectation",
        [
            ([0, 1], "1", [0, 2], pytest.raises(TypeError)),
            ([0, 1], [1], [0, 2], pytest.raises(TypeError)),
            ([0, 1], {1}, [0, 2], pytest.raises(TypeError)),
            ([0, 1], 2, [0, 2], pytest.raises(IndexError)),
            ([0, 0], 1, [0, 1], does_not_raise()),
            ([0, 1], 1, [0, 2], does_not_raise()),
            ([0, 2], 1, [0, 3], does_not_raise()),
            ([0, 3], 1, [0, 4], does_not_raise()),
            ([0, 4], 1, [0, 5], does_not_raise()),
            ([0, 5], 1, [0, 6], does_not_raise()),
            ([0, 6], 1, [0, 7], does_not_raise())
        ]
    )
    def test_game_tie_break(self, scores, player, result, expectation):
        "Правильность добавления очков при тайбрейке гейме"
        set1 = Set(Match())
        set1.is_tie_break = True
        game = Game(set1)
        game.scores = scores
        with expectation:
            game.add_point(player)
            assert game.scores == result

    @pytest.mark.parametrize(
        "sets, player, result, is_match_over, expectation",
        [
            ([1, 1], 0, [2, 1], True, does_not_raise()),
            ([0, 1], 1, [0, 2], True, does_not_raise()),
            ([0, 1], 0, [1, 1], False, does_not_raise()),
            ([1, 1], "1", [1, 1], True, pytest.raises(TypeError)),
            ([1, 1], [1], [1, 1], True, pytest.raises(TypeError)),
            ([1, 1], {1}, [1, 1], True, pytest.raises(TypeError)),
            ([1, 1], 2, [1, 1], True, pytest.raises(IndexError)),
        ]
    )
    def test_match_winner(self, sets, player, result, is_match_over, expectation):
        "Проверка, что матч завершается правильно"
        match = Match()
        match.sets = sets
        with expectation:
            match.add_set(player)
            assert match.sets == result
            assert match.is_match_over(player) == is_match_over

# Добавить проверкку введения неправильных значений.
