from sqlalchemy import String, ForeignKey
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


class MatchesOrm(Base):
    __tablename__ = "Matches"
    ID: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    UUID: Mapped[str] = mapped_column(String(50), unique=True)
    Player1: Mapped[int] = mapped_column(ForeignKey("Players.ID", ondelete="CASCADE"),
                                         nullable=False)
    Player2: Mapped[int] = mapped_column(ForeignKey('Players.ID', ondelete="CASCADE"),
                                         nullable=False)
    Winner: Mapped[int] = mapped_column(ForeignKey('Players.ID', ondelete="CASCADE"),
                                        nullable=True)
    Score: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"""Match={self.ID},
        UUID={self.UUID},
        Player1={self.Player1},
        Player2={self.Player2},
        Winner={self.Winner},
        Score={self.Score}"""
