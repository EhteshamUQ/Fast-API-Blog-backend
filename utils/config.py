import os
from dotenv import load_dotenv


load_dotenv()


class Configuration:
    PROJECT_TITLE = "Blog App"
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "blogDB")
    SQLALCHEMY_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

    JWT_KEY = os.environ.get("JWT_KEY")
    expiry_time = int(os.environ.get("EXPIRY_TIME"))
