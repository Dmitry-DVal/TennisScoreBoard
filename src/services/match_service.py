import logging
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import aliased

from src.database import session
from src.models.match_model import MatchesOrm
from src.models.player_model import PlayerOrm
from src.services.scoring_service import Match

logger = logging.getLogger("app_logger")


class MatchService:
    def create_match(self, id_first_player: int, id_second_player: int) -> MatchesOrm:
        """Создает матч"""
        with session() as db_session:
            match_uuid = str(uuid4())
            match = MatchesOrm(
                UUID=match_uuid, Player1=id_first_player,
                Player2=id_second_player,
                Score={"sets": [0, 0], "games": [0, 0], "points": [0, 0]}
            )

            db_session.add(match)
            db_session.commit()
            db_session.refresh(match)  # Обновляем объект, чтобы он не был "detached"
        return match

    def get_match_by_uuid(self, match_id: str) -> MatchesOrm | None:
        """Извлекает матч из БД по UUID и преобразует `Score` в словарь"""
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            return match  # Явно возвращаем match, даже если None

    def update_match_score(self, match_id: str, player: str) -> MatchesOrm | None:
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            if not match:
                return None

            match_obj = Match.from_dict(match.Score)

            match_obj.set_obj.game_obj.add_point(player)

            self.check_match_completion(match_id, player, match_obj)

            return match

    def check_match_completion(self, match_id: str, player: str, match_obj) -> None:
        with session() as db_session:
            match = db_session.query(MatchesOrm).filter_by(UUID=match_id).first()
            if match_obj.state.is_match_over:
                winner_id = match.Player1 if player == 0 else match.Player2  # Находим реальный ID игрока
                db_session.query(MatchesOrm).filter_by(UUID=match_id).update(
                    {"Score": match_obj.to_dict(), "Winner": winner_id}
                )
            else:
                db_session.query(MatchesOrm).filter_by(UUID=match_id).update(
                    {"Score": match_obj.to_dict()}
                )
            db_session.commit()


    def build_match_query(self, db_session, player_name=None):
        """Формирует базовый SQL-запрос для поиска завершённых матчей."""
        Player1 = aliased(PlayerOrm)
        Player2 = aliased(PlayerOrm)
        Winner = aliased(PlayerOrm)

        query = db_session.query(
            Player1.Name.label("player1"),
            Player2.Name.label("player2"),
            Winner.Name.label("winner"),
            MatchesOrm.Score["sets"].label("score_sets")
        ).join(Player1, MatchesOrm.Player1 == Player1.ID
               ).join(Player2, MatchesOrm.Player2 == Player2.ID
                      ).join(Winner, MatchesOrm.Winner == Winner.ID
                             ).filter(MatchesOrm.Winner.isnot(None))

        # 🔥 Исправляем поиск по имени (учитываем регистр и частичное совпадение)
        if player_name:
            player_name = f"%{player_name.lower()}%"  # 👈 Исправлено
            query = query.filter(
                (func.lower(Player1.Name).like(player_name)) |
                (func.lower(Player2.Name).like(player_name))
            )

        return query

    def paginate_query(self, query, page, per_page):
        """Добавляет пагинацию к SQL-запросу."""
        total_matches = query.count()
        total_pages = max(1, -(-total_matches // per_page))  # Округляем вверх
        matches = query.limit(per_page).offset((page - 1) * per_page).all()
        return matches, total_pages

    def get_completed_matches(self, player_name=None, page=1, per_page=5):
        """Возвращает завершенные матчи с поиском и пагинацией."""
        with session() as db_session:
            query = self.build_match_query(db_session, player_name)
            return self.paginate_query(query, page, per_page)
