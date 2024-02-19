from utils.config import Configuration
from sqlmodel import create_engine, Session as SqlModelSession, SQLModel

SQl_ALCHEMY_URL = Configuration.SQLALCHEMY_URL

engine = create_engine(SQl_ALCHEMY_URL, echo=True)


def get_db_session():
    session = SqlModelSession(engine)
    try:
        yield session
    finally:
        session.close()


def create_tables() -> None:
    SQLModel.metadata.create_all(bind=engine)
