import logging

from typing import Any
from tennis_app.core.match_state import MatchState

logger = logging.getLogger("app_logger")


class Match:
    """Service for calculating points in a match."""

    def __init__(self, state: MatchState):
        self.state = state
        self.set_obj = Set(self)

    def add_set(self, player: int) -> bool:
        self.state.sets[player] += 1
        logger.debug(f"Player  {player} wins a set.")
        logger.debug("Match score: %s", self.state.to_dict())

        if self.state.sets[player] == 2:
            self.state.is_match_over = True  # Завершаем матч
            logger.debug("The match is over! Winner: Player %s", player)

        return self.state.is_match_over

    def is_match_over(self, player: int) -> bool:
        return self.state.sets[player] == 2

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Match":
        return cls(MatchState(data))

    def to_dict(self) -> dict[str, Any]:
        return self.state.to_dict()


class Set:
    def __init__(self, match: Match):
        self.match = match
        self.state = match.state
        self.game_obj = Game(self)

    def add_game(self, player: int) -> None:
        self.state.games[player] += 1
        logger.debug(f"Player  {player} wins a game.")
        logger.debug("Match score: %s", self.state.to_dict())
        if self.is_won_set(player):
            self.match.add_set(player)
            self.drop_games()

    def is_won_set(self, player: int) -> bool:
        if self.state.games[player] == 6 and self.state.games[1 - player] < 5:
            return True
        if self.state.games == [6, 6]:
            self.state.is_tie_break = True
            logger.debug("Playing tiebreak: %s", self.state.to_dict())
            return False
        if self.state.games[player] == 7:
            return True
        return False

    def drop_games(self) -> None:
        self.state.games = [0, 0]
        self.state.is_tie_break = False
        self.game_obj.drop_point()


class Game:
    def __init__(self, set_obj: Set):
        self.set_obj = set_obj
        self.state = set_obj.state

    def drop_point(self) -> None:
        self.state.points = [0, 0]

    def add_point(self, player: int) -> None:
        if self.state.is_match_over:
            logger.warning("The game is over. Players can no longer get a point.")
            return

        if self.state.is_tie_break:
            self.play_tie_break(player)
        else:
            self.play_game(player)

    def play_tie_break(self, player: int) -> None:
        self.state.points[player] += 1  # type: ignore[operator]
        logger.debug("Tiebreak score: %s", self.state.to_dict())
        if (
            self.state.points[player] >= 7  # type: ignore[operator]
            and (self.state.points[player] - self.state.points[1 - player]) >= 2  # type: ignore[operator]
        ):
            self.set_obj.add_game(player)

    def play_game(self, player: int) -> None:
        point = self.state.points[player]  # type: ignore[operator]

        if point == 30:
            self.state.points[player] = 40  # type: ignore[operator]
        elif point == 40:
            self._handle_forty_score(player)
        elif point == "ad":
            self.state.points[player] = 60  # type: ignore[operator]
            self.set_obj.add_game(player)
            self.drop_point()
        elif isinstance(point, int):
            self.state.points[player] += 15  # type: ignore[operator]

        logger.debug("Game score: %s", self.state.to_dict())

    def _handle_forty_score(self, player: int) -> None:
        if self.state.points[1 - player] == "ad":
            self.state.points = [40, 40]
        elif self.state.points[1 - player] < 40:  # type: ignore[operator]
            self.state.points[player] += 20  # type: ignore[operator]
            self.set_obj.add_game(player)
            self.drop_point()
        elif self.state.points == [40, 40]:
            self.state.points[player] = "ad"
