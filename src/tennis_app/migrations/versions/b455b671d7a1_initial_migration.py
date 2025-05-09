"""Initial migration

Revision ID: b455b671d7a1
Revises:
Create Date: 2025-03-10 22:25:28.511279

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "b455b671d7a1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Players",
        sa.Column("ID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("ID"),
    )
    op.create_table(
        "Matches",
        sa.Column("ID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UUID", sa.String(length=50), nullable=False),
        sa.Column("Player1", sa.Integer(), nullable=False),
        sa.Column("Player2", sa.Integer(), nullable=False),
        sa.Column("Winner", sa.Integer(), nullable=True),
        sa.Column("Score", mysql.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["Player1"], ["Players.ID"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["Player2"], ["Players.ID"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["Winner"], ["Players.ID"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("ID"),
        sa.UniqueConstraint("UUID"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Matches")
    op.drop_table("Players")
    # ### end Alembic commands ###
