from sqlmodel import create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    from app.models.hero_models import SQLModel  # import all models here

    SQLModel.metadata.create_all(engine)
