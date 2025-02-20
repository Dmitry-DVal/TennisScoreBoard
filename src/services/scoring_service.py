class Match:
    def __init__(self):
        self.sets = [0, 0]

    def add_set(self, player: int) -> bool:
        self.sets[player] += 1
        print(f"Счет матча: {self.sets}")
        return True if self.is_match_over(player) else False

    def is_match_over(self, player: int) -> bool:
        if self.sets[player] == 2:
            print(f"Матч выиграл игрок {player + 1}. Счет {self.sets}")
            return True
        else:
            return False


class Set:
    def __init__(self, match_obj: Match):
        self.games = [0, 0]
        self.match_obj = match_obj
        self.is_tie_break = False

    def add_game(self, player: int) -> None:
        self.games[player] += 1
        print(f"Счет сета: {self.games}")
        if self.is_won_set(player):
            self.match_obj.add_set(player)

    def is_won_set(self, player: int) -> bool:
        """Проверяет, выигран ли сет"""
        if self.games[player] == 6 and self.games[1 - player] < 5:
            print(f"Сет выиграл игрок {player + 1}")
            return True
        if self.games == [6, 6]:
            print(f'Счет {self.games}, играем Тайбрейк')
            self.is_tie_break = True
            return False
        if self.games[player] == 7:
            print(f"Сет выиграл игрок {player + 1}")
            return True
        return False


class Game:
    def __init__(self, set_obj: Set):
        self.scores = [0, 0]
        self.set_obj = set_obj

    def add_point(self, player: int) -> None:
        if self.set_obj.is_tie_break:
            self.play_tie_break(player)
        else:
            self.play_game(player)

    def play_tie_break(self, player: int) -> int | None:
        self.scores[player] += 1
        print(f"Счет Тай брейка: {self.scores}")
        if self.scores[player] >= 7 and (
                self.scores[player] - self.scores[1 - player]) >= 2:
            print(
                f"Тай брейк выиграл игрок {self.scores.index(self.scores[player]) + 1}")
            self.set_obj.add_game(player)
        return

    def play_game(self, player: int) -> int | None:
        if self.scores[player] == 30:
            self.scores[player] += 10
        elif self.scores[player] == 40:
            self._handle_forty_score(player)
        elif self.scores[player] == 'ad':
            self.scores[player] = 60
            print(f"Счет гейма: {self.scores}")
            self.set_obj.add_game(player)
            return player
        else:
            self.scores[player] += 15
        print(f"Счет гейма: {self.scores}")

    def _handle_forty_score(self, player: int) -> int | None:
        if self.scores[1 - player] == 'ad':
            self.scores = [40, 40]
        elif self.scores[1 - player] < 40:
            self.scores[player] += 20
            print(f"Счет гейма: {self.scores}")
            self.set_obj.add_game(player)
            return player
        elif self.scores == [40, 40]:
            self.scores[player] = 'ad'
