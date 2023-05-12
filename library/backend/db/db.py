from sqlalchemy import create_engine

from backend.db.models import Base
from backend.db.settings import DBSettings

settings = DBSettings()


def init_db():
    
    engine = create_engine(f"postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}")
    Base.metadata.create_all(bind=engine)
