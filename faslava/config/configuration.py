from pydantic import BaseModel
from faslava.enums.enums import EnvEnum
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseBackend(BaseModel):
    name: str
    protocol: str
    default_port: int


SUPPORTED_DATABASE_BACKENDS = {
    "postgresql": DatabaseBackend(
        name="postgresql", protocol="postgresql", default_port=5432
    ),
    "sqlite": DatabaseBackend(name="sqlite", protocol="sqlite", default_port=-1),
}


class Settings(BaseSettings):
    """
    A settings class containing the application configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AR_",  # Prefix for env variables identification.
        extra="ignore",  # Default: "forbid"
    )

    DEBUG: bool
    ENV: EnvEnum
    DB_NAME: str
    DB_HOST: str
    DB_USER: str = ""
    DB_PWD: str = ""
    DB_PORT: int = 0
    DB_ENGINE: str
    ALEMBIC_CUSTOM_SCHEMA: str = "almbc"

    def build_db_url(self):
        if self.DB_ENGINE not in SUPPORTED_DATABASE_BACKENDS:
            raise Exception("Database engine is not supported.")

        print("DB_ENDING:", self.DB_ENGINE)
        print("IS PSQL:", self.DB_ENGINE == "postgresql")
        if self.DB_ENGINE == "postgresql":
            backend = SUPPORTED_DATABASE_BACKENDS["postgresql"]
            url_pwd_string = f":{self.DB_PWD}" if self.DB_PWD else ""
            return f"postgresql://{self.DB_USER}{url_pwd_string}@{self.DB_HOST}:{self.DB_PORT or backend.default_port}/{self.DB_NAME}"

        print("IS SQLITE:", self.DB_ENGINE == "sqlite")
        if self.DB_ENGINE == "sqlite":
            return f"sqlite:///{self.DB_NAME}"

        raise Exception("Database backend not supported!")


settings = Settings()
