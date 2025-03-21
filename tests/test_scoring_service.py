from contextlib import nullcontext as does_not_raise

import pytest

from tennis_app.services import MatchState, Match


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
        """The correctness of adding games in a set."""
        match = Match(MatchState({"sets": [0, 0], "games": games, "points": [0, 0]}))
        match.set_obj.games = games
        with expectation:
            match.set_obj.add_game(player)
            assert match.set_obj.games == result
            assert match.state.is_tie_break == is_tie_break

    @pytest.mark.parametrize(
        "points, player, result, expectation",
        [
            ([40, 40], 1, [40, 'ad'], does_not_raise()),
            ([40, 40], 0, ['ad', 40], does_not_raise()),
            ([15, 40], 1, [0, 0], does_not_raise()),
            ([40, 'ad'], 1, [0, 0], does_not_raise()),
            (['ad', 40], 1, [40, 40], does_not_raise()),
            (['ad', 40], 0, [0, 0], does_not_raise()),
            ([0, 0], 0, [15, 0], does_not_raise()),
            ([15, 0], 0, [30, 0], does_not_raise()),
            ([30, 0], 0, [40, 0], does_not_raise()),
            ([40, 0], 0, [0, 0], does_not_raise()),
            ([0, 15], "1", [0, 15], pytest.raises(TypeError)),
            ([0, 15], [1], [0, 15], pytest.raises(TypeError)),
            ([0, 15], {1}, [0, 15], pytest.raises(TypeError)),
            ([0, 15], 2, [0, 15], pytest.raises(IndexError)),
        ]
    )
    def test_game_add_point(self, points, player, result, expectation):
        """Correctness of adding points at a standard game."""
        match = Match(MatchState({"sets": [0, 0], "points": points}))
        match.state.games = points
        with expectation:
            match.set_obj.game_obj.add_point(player)
            assert match.state.points == result

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
            ([0, 6], 1, [0, 7], does_not_raise()),
        ]
    )
    def test_game_tie_break(self, scores, player, result, expectation):
        """Correctness of adding points in a tiebreak game."""
        match = Match(MatchState({"sets": [0, 0], "games": [0, 0], "points": scores}))
        match.state.is_tie_break = True

        with expectation:
            match.set_obj.game_obj.add_point(player)
            assert match.state.points == result

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
        """Checking that the match ends correctly."""
        match = Match(MatchState({"sets": sets, "points": [0, 0]}))
        with expectation:
            match.add_set(player)
            assert match.state.sets == result
            assert match.is_match_over(player) == is_match_over
