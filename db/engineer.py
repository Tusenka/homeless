import os
from contextlib import contextmanager
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

import logging

logger = logging.getLogger(__name__)


class DbEngine:
    """Настройки базы данных и подключения к ней."""

    def __init__(self):
        self.db_url = os.getenv("DB_CONNECTION")
        self.engine = create_engine(
            self.db_url, echo=True, isolation_level="READ COMMITTED"
        )

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )

    @contextmanager
    def get_session(self):
        try:
            session = self.SessionLocal()
            yield session
            session.commit()

        except Exception as e:
            logger.error(
                f"Can't commit the session. Error: {e}. The session will be rollbacked"
            )
            session.rollback()
            raise

        finally:
            session.close()
