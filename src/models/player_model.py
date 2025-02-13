from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class PlayersOrm(Base):
    __tablename__ = "Players"
    ID: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    Name: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"Player: (id = {self.ID}, name = {self.Name})"

    # Зависимости
    matches_as_player1 = relationship("MatchesOrm",
                                      foreign_keys="[MatchesOrm.Player1]")
    matches_as_player2 = relationship("MatchesOrm",
                                      foreign_keys="[MatchesOrm.Player2]")
    matches_as_winner = relationship("MatchesOrm",
                                     foreign_keys="[MatchesOrm.Winner]")
