"""API middleware"""
from loguru import logger
from config import settings


def setup_logging():
    """Setup logging configuration"""
    logger.add(
        settings.log_file,
        rotation="10 MB",
        retention="1 week",
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )



