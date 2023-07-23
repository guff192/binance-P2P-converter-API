from sys import stderr
from loguru import logger


# removing default stderr logger
logger.remove()

# logging debug logs to a file
logger.add(
    sink="app.log",
    level="DEBUG",
    format='{time:DD.MM.YYYY HH:mm:ss.SSS} | {level} | {message}',
    rotation="500 MB",
    compression="zip",
    backtrace=True,
    diagnose=True,
)

# logging errors to stderr
logger.add(
    sink=stderr,
    level="ERROR",
    colorize=True
)

