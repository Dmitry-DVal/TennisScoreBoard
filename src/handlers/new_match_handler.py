import urllib.parse

from pydantic import ValidationError

from src.dtos.player_dto import PlayerDTO
from src.exceptions import DateValidationError
from src.handlers import RequestHandler, logger
from src.services import MatchService, PlayerService


class NewMatchHandler(RequestHandler):
    """Обработчик страницы создания нового матча."""

    def handle_get(self, environ, start_response):
        response_body = self.render_template("new_match.html")
        return self.make_response(start_response, response_body)

    @RequestHandler.exception_handler
    def handle_post(self, environ, start_response):
        try:
            request_body = environ['wsgi.input'].read().decode('utf-8')
            logger.debug(f"Тело запроса {request_body}")
            data = urllib.parse.parse_qs(request_body)

            player1_dto, player2_dto = self._validate_players(data)
            if player1_dto.name == player2_dto.name:
                logger.warning(f"Имена игроков не могу быть одинаковыми. {player1_dto.name }, {player2_dto.name }")
                return self.handle_exception(start_response, DateValidationError(f"Игроки не могут быть одинаковыми. {data}"))

            player1, player2 = self._get_or_create_players(player1_dto, player2_dto)

            return self._create_and_redirect(player1, player2, start_response)

        except ValidationError:
            return self.handle_exception(start_response, DateValidationError(
                'first_player = second_player'))

    def redirect(self, start_response, location: str):
        """Редирект на другую страницу"""
        logger.info(f"Переадресация {location}")
        start_response("303 See Other", [("Location", location)])
        return []

    def _validate_players(self, data) -> tuple[PlayerDTO, PlayerDTO]:
        """Валидирует данные игроков."""
        first_player = data.get("first_player", [""])[0]
        second_player = data.get("second_player", [""])[0]

        player1 = PlayerDTO(name=first_player)
        player2 = PlayerDTO(name=second_player)

        logger.info(f"Валидация прошла успешно: {repr(player1)}, {repr(player2)}")
        return player1, player2

    def _get_or_create_players(self, player1_dto, player2_dto):
        """Находит или создает игроков в БД."""
        player1 = PlayerService().get_or_create_player(player1_dto.name)
        player2 = PlayerService().get_or_create_player(player2_dto.name)
        logger.debug(f"Игроки найдены или созданы: {player1}, {player2}")
        return player1, player2

    def _create_and_redirect(self, player1, player2, start_response):
        """Создает матч и делает редирект на страницу счета."""
        match = MatchService().create_match(player1.ID, player2.ID)
        logger.debug(f"Матч успешно создан: {match}")
        return self.redirect(start_response, f"/match-score?uuid={match.UUID}")
