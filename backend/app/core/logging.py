import logging
import sys

from loguru import logger

LOG_FORMAT = (
    "{time:YYYY-MM-DDTHH:mm:ss.SSSZ} | {level} | {name}:{function}:{line} | "
    "{extra[request_id]} | {message}"
)


def setup_logging() -> None:
    logging.getLogger().handlers = []
    logger.remove()
    logger.add(sys.stdout, format=LOG_FORMAT, backtrace=False, diagnose=False, enqueue=True)
