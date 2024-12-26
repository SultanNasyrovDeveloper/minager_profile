from logging import INFO
from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

type DBDriver = Literal["postgresql+asyncpg", "postgresql", "motor", "surreal"]


class AMQPConfig(BaseSettings):
    host: str = "localhost"
    port: str = "5672"
    username: str
    password: SecretStr
    virtual_host: str = "vhost"
    exchange: str

    def url(self) -> str:
        return str(
            URL.build(
                scheme="amqp",
                user=self.username,
                password=self.password.get_secret_value(),
                host=self.host,
                port=int(self.port),
                path="/" + self.virtual_host,
            )
        )


class DBConnection(BaseModel):
    driver: DBDriver = "postgresql+asyncpg"
    name: str
    namespace: str | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: SecretStr | None = None


class LoggingConfig(BaseSettings):
    level: int = INFO
    format: str = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    # datetime_format: str = ''

    def to_basic_config(self) -> dict:
        return {
            "level": self.level,
            "format": self.format,
            # 'datefmt': self.datetime_format
        }


class ApplicationSettings(BaseSettings):
    debug: bool = False
    db: DBConnection
    user_events_routing_key: str
    user_events_queue: AMQPConfig
    logging: LoggingConfig = LoggingConfig()

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"), env_nested_delimiter="__"
    )
