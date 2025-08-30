import sys
from loguru import logger


def get_logger():
    logger.remove()
    logger.add(
        sink=sys.stdout, format="<level>{level}</level>: {message}", colorize=True
    )
    return logger
