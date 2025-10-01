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


def get_engine():
    """
    Create engine based on the type of database.

    Returns engine conditionally as per the database.
    The db URL needs to be changed in the .env file.
    """
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        engine = create_engine(
            settings.database_url,
            echo=True,
            connect_args=connect_args,  # only for sqlite
        )  # for sqlite
        return engine
    elif settings.database_url.startswith("postgresql"):
        engine = create_engine(
            settings.database_url,
            echo=True,
        )  # for postgres
        return engine
    else:
        message = f"Invalid {settings.database_url}"
        raise ValueError(message)


engine = get_engine()


def create_db_and_tables():
    """
    Create db and tables.

    Create db (for sqlite only) (if postgres, first create a db manually in pgadmin).
    Create tables
    """
    from app.models.hero_models import SQLModel  # import all models here

    SQLModel.metadata.create_all(engine)
