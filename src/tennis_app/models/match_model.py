from uuid import uuid4

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import mapped_column, Mapped

from tennis_app.database import Base


class MatchesOrm(Base):
    __tablename__ = "Matches"
    ID: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    UUID: Mapped[str] = mapped_column(String(50), unique=True, default=lambda: str(
        uuid4()))

    Player1: Mapped[int] = mapped_column(ForeignKey("Players.ID", ondelete="CASCADE"),
                                         nullable=False)
    Player2: Mapped[int] = mapped_column(ForeignKey('Players.ID', ondelete="CASCADE"),
                                         nullable=False)
    Winner: Mapped[int] = mapped_column(ForeignKey('Players.ID', ondelete="CASCADE"),
                                        nullable=True)
    Score: Mapped[dict] = mapped_column(JSON)

    def __repr__(self):
        return f"""Match={self.ID},
        UUID={self.UUID},
        Player1={self.Player1},
        Player2={self.Player2},
        Winner={self.Winner},
        Score={self.Score}"""
