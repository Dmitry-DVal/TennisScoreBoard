import logging

from src.services.match_state import MatchState

logger = logging.getLogger("app_logger")


class Match:
    def __init__(self, state: MatchState):
        self.state = state
        self.set_obj = Set(self)

    def add_set(self, player: int) -> bool:
        self.state.sets[player] += 1
        logger.debug(f"Игрок {player} выиграл сет")
        logger.debug(f"Счет матча: {self.state.to_dict()}")

        if self.state.sets[player] == 2:
            self.state.is_match_over = True  # Завершаем матч
            logger.debug(f"Матч завершён! Победитель: Игрок {player}")

        return self.state.is_match_over

    def is_match_over(self, player: int) -> bool:
        return self.state.sets[player] == 2

    @classmethod
    def from_dict(cls, data: dict):
        return cls(MatchState(data))

    def to_dict(self):
        return self.state.to_dict()


class Set:
    def __init__(self, match: Match):
        self.match = match
        self.state = match.state
        self.game_obj = Game(self)

    def add_game(self, player: int) -> None:
        self.state.games[player] += 1
        logger.debug(f"Игрок {player} выиграл гейм")
        logger.debug(f"Счет сета: {self.state.to_dict()}")
        if self.is_won_set(player):
            self.match.add_set(player)
            self.drop_games()

    def is_won_set(self, player: int) -> bool:
        if self.state.games[player] == 6 and self.state.games[1 - player] < 5:
            return True
        if self.state.games == [6, 6]:
            self.state.is_tie_break = True
            logger.debug(f"Играем Тайбрейк: {self.state.to_dict()}")
            return False
        if self.state.games[player] == 7:
            return True
        return False

    def drop_games(self):
        self.state.games = [0, 0]
        self.state.is_tie_break = False
        self.game_obj.drop_point()


class Game:
    def __init__(self, set_obj: Set):
        self.set_obj = set_obj
        self.state = set_obj.state

    def drop_point(self):
        self.state.points = [0, 0]

    def add_point(self, player: int) -> None:

        if self.state.is_match_over:
            logger.warning(f"Игра окончена. Игрок {player} не может получить очко.")
            return

        if self.state.is_tie_break:
            self.play_tie_break(player)
        else:
            self.play_game(player)

    def play_tie_break(self, player: int) -> None:
        self.state.points[player] += 1
        logger.debug(f"Счет Тайбрейка: {self.state.to_dict()}")
        if self.state.points[player] >= 7 and (
                self.state.points[player] - self.state.points[1 - player]) >= 2:
            self.set_obj.add_game(player)

    def play_game(self, player: int) -> None:
        if self.state.points[player] == 30:
            self.state.points[player] += 10
        elif self.state.points[player] == 40:
            self._handle_forty_score(player)
        elif self.state.points[player] == "ad":
            self.state.points[player] = 60
            self.set_obj.add_game(player)
            self.drop_point()
        else:
            self.state.points[player] += 15
        logger.debug(f"Счет гейма: {self.state.to_dict()}")

    def _handle_forty_score(self, player: int) -> None:
        if self.state.points[1 - player] == "ad":
            self.state.points = [40, 40]
        elif self.state.points[1 - player] < 40:
            self.state.points[player] += 20
            self.set_obj.add_game(player)
            self.drop_point()
        elif self.state.points == [40, 40]:
            self.state.points[player] = "ad"
