from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.logger import logger
from app.core.settings import app_settings

Base = type("Base", (DeclarativeBase,), {})
engine = create_engine(app_settings.postgres_database_url)
SessionLocal = sessionmaker(engine, class_=Session, expire_on_commit=False)


def get_session():
    with SessionLocal() as session:
        yield session


def check_db_connection() -> bool:
    with SessionLocal() as session:
        try:
            return bool(session.execute(text("SELECT 1")))
        except ConnectionError as error:
            logger.critical(f"Postgres connection error: {error}")
    return False