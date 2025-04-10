import sys
import logging

def build_logger(name: str, level: int = logging.INFO, output=sys.stdout) -> logging.Logger:
    """
    Builds and returns a logger with the specified name, level, and output.

    Args:
        name (str): The name of the logger.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
        output: The output stream (e.g., sys.stdout or a file object).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        handler = logging.StreamHandler(output)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    return logger