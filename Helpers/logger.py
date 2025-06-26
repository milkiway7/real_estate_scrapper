import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        # File handler
        file_handler = logging.FileHandler("logs/app.log", mode='w', encoding='utf-8')
        file_handler.setFormatter(stream_formatter)
        logger.addHandler(file_handler)

        logger.propagate = False

    return logger
