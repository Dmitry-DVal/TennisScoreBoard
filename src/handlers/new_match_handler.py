import urllib.parse

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.dtos.player_dto import PlayerDTO
from src.handlers.base_handler import BaseHandler, logger
from src.services.match_service import MatchService
from src.services.player_service import PlayerService


class NewMatchHandler(BaseHandler):
    """Обработчик страницы создания нового матча."""

    def handle_request(self, environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET")
        if method == "POST":
            return self.handle_post(environ, start_response)
        else:
            return self.handle_get(start_response)

    def handle_get(self, start_response):
        response_body = self.render_template("new_match.html")
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body]

    def handle_post(self, environ, start_response):
        try:
            request_body = environ['wsgi.input'].read().decode('utf-8')
            logger.debug(f"Тело запроса {request_body}")
            data = urllib.parse.parse_qs(request_body)
            logger.debug(data)

            first_player = data.get("first_player")[0]
            second_player = data.get("second_player")[0]
            # Валидация данных
            player1 = PlayerDTO(name=first_player)
            player2 = PlayerDTO(name=second_player)
            logger.info(
                f"Валидация данных прошла успешно {repr(player1)}, {repr(player2)}")

            # Проверка игроков в БД
            player1 = PlayerService().get_or_create_player(player1.name)
            player2 = PlayerService().get_or_create_player(player2.name)
            logger.debug(f"Игроки найдены или созданы: {player1}, {player2}")

            # Создание матча
            match = MatchService().create_match(player1.ID, player2.ID)
            logger.debug(f"Матч успешно создан: {match}")

            # Отправка ответа
            start_response("303 See Other",
                           [("Location", f"/match-score?uuid={match.UUID}")])
            return []
        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e.errors()}")
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            # print(e.errors(include_url=False))
            return [f'{{"error": "{e.errors(include_url=False)}"}}'.encode("utf-8")]
        except IntegrityError as e:
            logger.error("Ошибка в БД: дублирование данных или нарушение связей")
            start_response("500 Internal Server Error",
                           [("Content-Type", "text/plain")])
            return [f"Ошибка сервера при работе с БД".encode("utf-8")]
        except Exception as e:
            logger.exception("Неизвестная ошибка")
            start_response("500 Internal Server Error",
                           [("Content-Type", "text/plain")])
            return [f"Внутренняя ошибка сервера".encode("utf-8")]
