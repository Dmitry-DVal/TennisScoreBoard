from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from tennis_app.config import settings_db

engine = create_engine(url=settings_db.DATABASE_URL_pymysql, echo=False)


class Base(DeclarativeBase):
    pass


session = sessionmaker(bind=engine, expire_on_commit=False)
