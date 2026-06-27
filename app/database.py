import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv


load_dotenv()


class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise ValueError("DATABASE_URL não configurada no .env")

        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_db(self):
        db = self.SessionLocal()

        try:
            yield db
        finally:
            db.close()


Base = declarative_base()
database = Database()