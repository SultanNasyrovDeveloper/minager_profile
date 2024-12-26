import logging

from .app import settings

logging.basicConfig(**settings.logging.to_basic_config())
logging.getLogger("websockets").setLevel(logging.DEBUG)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
