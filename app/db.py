from functools import lru_cache

from sqlmodel import create_engine

from app.config import Settings

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"


@lru_cache
def get_settings():
    settings = Settings()
    return settings


settings = get_settings()

connect_args = {"check_same_thread": False}
# engine = create_engine(settings.database_url, echo=True, connect_args=connect_args)
engine = create_engine(settings.database_url, echo=True)


def create_db_and_tables():
    from app.models.hero_models import SQLModel  # import all models here

    SQLModel.metadata.create_all(engine)
