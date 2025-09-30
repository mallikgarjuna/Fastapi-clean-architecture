from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # First: Create these variables in .env file
    # Check with this:
    db_engine: str = "sqlite"  # default db; (sqlite/ postgres)

    # sqlite settings (read from .env file)
    sqlite_file_name: str = "database.db"

    # read env vars from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        if self.db_engine == "sqlite":
            if not self.sqlite_file_name:
                raise ValueError(
                    "SQLITE_FILE_NAME must be set when DB_ENGINE=sqlite in .env file",
                )
        return f"sqlite:///{self.sqlite_file_name}"


# Test with interactive ipynb in vscode itself (using Shift + Enter)
if __name__ == "__main__":
    settings = Settings()
    print(settings.sqlite_file_name)  # dabase.db
    print(settings.database_url)  # sqlite:///dabase.db
