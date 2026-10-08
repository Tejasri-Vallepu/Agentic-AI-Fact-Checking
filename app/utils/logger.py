from pathlib import Path

from loguru import logger

from app.core.config import settings


def configure_logging():
    log_directory = Path(settings.logs_path)
    log_directory.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sink=lambda message: print(message, end=""),
        level=settings.LOG_LEVEL,
    )

    logger.add(
        log_directory / "agentic_fact_checker.log",
        rotation="10 MB",
        retention="7 days",
        level=settings.LOG_LEVEL,
        enqueue=True,
    )

    return logger
