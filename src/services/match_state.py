from typing import Dict, Union


class MatchState:
    def __init__(self, data: Dict[str, Union[int, list]]):
        self.data = data

    @property
    def sets(self) -> list[int]:
        return self.data["sets"]

    @sets.setter
    def sets(self, value: list[int]):
        self.data["sets"] = value

    @property
    def games(self) -> list[int]:
        return self.data["games"]

    @games.setter
    def games(self, value: list[int]):
        self.data["games"] = value

    @property
    def points(self) -> list[int]:
        return self.data["points"]

    @points.setter
    def points(self, value: list[int]):
        self.data["points"] = value

    @property
    def is_tie_break(self) -> bool:
        return self.data.get("is_tie_break", False)

    @is_tie_break.setter
    def is_tie_break(self, value: bool):
        self.data["is_tie_break"] = value

    @property
    def is_match_over(self) -> bool:
        return bool(self.data.get("is_match_over", False))

    @is_match_over.setter
    def is_match_over(self, value: bool):
        self.data["is_match_over"] = value

    def to_dict(self) -> Dict[str, Union[int, list]]:
        return self.data
