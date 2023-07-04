from sqlalchemy import create_engine
from pydantic import BaseSettings
from sqlalchemy.orm import declarative_base, Session


class EnvDBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file = "backend/.env"


settings = EnvDBSettings()
DATABASE_URL = f"postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"
DB_ENGINE = create_engine(DATABASE_URL)
Base = declarative_base()

def initialization_database():
    Base.metadata.create_all(bind=DB_ENGINE)

def get_session():
    with Session(DB_ENGINE) as session:
        yield session