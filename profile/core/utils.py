from profile.settings import DBConnection

from yarl import URL


def make_database_url(config: DBConnection, **additional) -> str:
    return str(
        URL.build(
            scheme=config.driver,
            user=config.username,
            password=config.password.get_secret_value(),
            host=config.host,
            port=config.port,
            path="/" + config.name,
            **additional,
        )
    )
