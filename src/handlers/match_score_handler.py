from src.handlers.base_handler import BaseHandler, logger
from src.services.match_service import MatchService
from src.services.player_service import PlayerService


class MatchScoreHandler(BaseHandler):
    def __init__(self):
        self.match_service = MatchService()
        self.player_service = PlayerService()

    def make_response(self, response_body: str, start_response, status="200 OK"):
        """Формирует HTTP-ответ"""
        start_response(status, [("Content-Type", "text/html; charset=utf-8")])
        return [response_body]

    def handle_request(self, environ, start_response):
        if environ["REQUEST_METHOD"] == "POST":
            return self.handle_post(environ, start_response)
        return self.handle_get(environ, start_response)

    def handle_get(self, environ, start_response):
        """Обрабатывает GET-запрос и рендерит страницу матча."""
        match_id = self.match_service.get_uuid_from_request(environ)
        match = self.match_service.get_match_by_uuid(match_id)

        logger.debug(f"Запрос имен игроков, счета у сервиса для рендеринга страниц")

        if not match:
            response_body = "Match not found"
            logger.debug("Match not found, 404 Not Found")
            return self.make_response(response_body,
                                      start_response,
                                      status="404 Not Found")

        # Получаем имена игроков по их ID
        player1_name, player2_name = self.player_service.get_players_name_by_id(
            match.Player1,
            match.Player2
        )
        logger.debug(f"{player1_name, player2_name}"
                     f"{match.Score}")

        response_body = self.render_template(
            "match_score.html",
            match=match,
            player1_name=player1_name,
            player2_name=player2_name
        )

        return self.make_response(response_body, start_response)

    def handle_post(self, environ, start_response):
        """Обрабатывает POST-запрос: обновляет счёт и рендерит обновлённую страницу."""
        match_id = self.match_service.get_uuid_from_request(environ)
        form_data = self.match_service.get_form_data(environ)
        # logger.debug(f"form_data = {form_data}")
        logger.debug(f"match_id = {match_id},"
                     f"form_data = {form_data}")

        if "player" not in form_data:
            response_body = "Invalid request"
            logger.debug("Invalid request, 400 Bad Request")

            return self.make_response(response_body, start_response,
                                      status="400 Bad Request")

        updated_match = self.match_service.update_match_score(match_id,
                                                              form_data["player"])
        logger.debug(f"updated_match = {updated_match}")
        if not updated_match:
            response_body = "Match not found"
