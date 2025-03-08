import json
import urllib.parse

from pydantic import ValidationError

from src.dtos.point_winner_dto import PointWinnerDTO
from src.exceptions import DateValidationError
from src.handlers.base_handler import RequestHandler, logger
from src.services.match_service import MatchService
from src.services.player_service import PlayerService


class MatchScoreHandler(RequestHandler):
    def __init__(self):
        self.match_service = MatchService()
        self.player_service = PlayerService()

    def handle_get(self, environ, start_response):
        """Обрабатывает GET-запрос и рендерит страницу матча."""
        match_id = self.get_uuid_from_request(environ)
        match = self.match_service.get_match_by_uuid(match_id)

        logger.debug(f"Запрос имен игроков, счета у сервиса для рендеринга страниц")

        if not match:
            return self.handle_exception(start_response, DateValidationError(match_id))

        match_score = self._get_match_score(match)
        player1_name, player2_name = self._get_player_names(match)

        response_body = self.render_template(
            "match_score.html",
            match=match,
            match_score=match_score,
            player1_name=player1_name,
            player2_name=player2_name
        )

        return self.make_response(start_response, response_body)

    @RequestHandler.exception_handler
    def handle_post(self, environ, start_response):
        """Обрабатывает POST-запрос: обновляет счёт и рендерит обновлённую страницу."""
        try:
            request_body = environ['wsgi.input'].read().decode('utf-8')
            logger.debug(f"Тело запроса {request_body}")
            data = urllib.parse.parse_qs(request_body)

            validated_data = PointWinnerDTO(player=data.get("player", [""])[0])
            logger.debug(f"Валидированные данные: {validated_data} - Выиграл очко")

            # Обновляем счёт матча
            match_id = self.get_uuid_from_request(environ)
            updated_match = self.match_service.update_match_score(
                match_id,
                validated_data.player
            )

            if not updated_match:
                return self.handle_exception(start_response,
                                             DateValidationError(match_id))

            return self.handle_get(environ, start_response)

        except ValidationError:
            return self.handle_exception(start_response, DateValidationError(data))

    def _get_match_score(self, match):
        """Извлекает и преобразует счёт матча."""
        return json.loads(match.Score) if isinstance(match.Score, str) else match.Score

    def _get_player_names(self, match):
        """Получает имена игроков по их ID."""
        return self.player_service.get_players_name_by_id(
            match.Player1,
            match.Player2
        )
