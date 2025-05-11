import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with the specified name or the default name if none is provided.
    
    Args:
        name (Optional[str]): The name of the logger. If None, the default name is used.
        
    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.propagate = False  # Zapobiega podwójnym logom w FastAPI/django

    return logger