import json
from uuid import uuid4

from src.database import session
from src.models.match_model import MatchesOrm
from src.services.scoring_service import Match, Set, Game


class MatchService:
    def create_match(self, id_first_player: int, id_second_player: int) -> MatchesOrm:
        """Создает матч"""
        with session() as db_session:
            match_uuid = str(uuid4())
            match = MatchesOrm(UUID=match_uuid, Player1=id_first_player,
                               Player2=id_second_player,
                               Score=
                               {"sets": [0, 0], "games": [0, 0], "points": [0, 0]}
                               # Score=json.dumps(
                               #     {"sets": [0, 0], "games": [0, 0], "points": [0, 0]})
                               )

            db_session.add(match)
            db_session.commit()
            db_session.refresh(match)  # Обновляем объект, чтобы он не был "detached"
        return match

    def get_uuid_from_request(self, environ):
        """Получает UUID матча из GET-параметров запроса"""
        query_string = environ.get("QUERY_STRING", "")
        params = dict(
            param.split("=") for param in query_string.split("&") if "=" in param)
        return params.get("uuid")

    def get_match_by_uuid(self, match_id):
        """Извлекает матч из БД по UUID и преобразует `Score` в словарь"""
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()

            if match:
                # match.Score = json.loads(match.Score)  # Декодируем строку в словарь
                match.Score = match.Score

            return match

    def get_form_data(self, environ):
        """Парсит `POST`-данные запроса"""
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0

        request_body = environ["wsgi.input"].read(request_body_size).decode("utf-8")
        return dict(
            param.split("=") for param in request_body.split("&") if "=" in param)

    def update_match_score(self, match_id: str, player: str):
        """Обновляет счёт матча, добавляя очко игроку."""
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            if not match:
                return None

            player = int(player)

            # # Загружаем счёт из JSON
            # match_score = json.loads(match.Score) if match.Score else {"sets": [0, 0],
            #                                                            "games": [0, 0],
            #                                                            "points": [0, 0]}
            match_score = match.Score if match.Score else {"sets": [0, 0],
                                                           "games": [0, 0],
                                                           "points": [0, 0]}

            # Обновляем очки через сервис
            game = Game(Set(Match()))
            game.scores = match_score["points"]
            game.add_point(player)

            # Сохраняем изменения обратно
            match_score["points"] = game.scores
            match.Score = json.dumps(
                match_score)  # 🔹 Сохраняем **весь** словарь, а не только points
            db_session.commit()
            return match

    def save_match(self, match):
        """Сохраняет обновлённый матч в БД"""
        with session() as db_session:
            db_session.add(match)
            db_session.commit()
