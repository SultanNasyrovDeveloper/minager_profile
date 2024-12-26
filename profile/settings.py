from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

type DBDriver = Literal["postgresql+asyncpg", "postgresql", "motor", "surreal"]


class DBConnection(BaseModel):
    driver: DBDriver = "postgresql+asyncpg"
    name: str
    namespace: str | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: SecretStr | None = None


class ApplicationSettings(BaseSettings):
    db: DBConnection

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"), env_nested_delimiter="__"
    )
