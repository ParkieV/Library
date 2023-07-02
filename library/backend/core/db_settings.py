from sqlalchemy import create_engine

from backend.db.models import Base
from backend.db.settings import DBSettings


settings = DBSettings()
DATABASE_URL = f"postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"

def initialization_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
