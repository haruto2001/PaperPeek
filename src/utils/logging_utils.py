import logging
import os
from typing import Optional


def get_logger(logger_name: str, log_path: Optional[str] = None) -> logging.Logger:
    """
    Creates and configures a logger that outputs to the console and optionally to a file.

    Args:
        logger_name (str): The name of the logger, useful for identifying different loggers.
        log_path (Optional[str]): Path to the log file. If None, logs will only be output to the console.

    Returns:
        logging.Logger: The configured logger object.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s %(filename)s %(funcName)s():%(lineno)s\n"
        "[%(levelname)s] %(message)s\n"
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_path is not None:
        log_dir = os.path.dirname(log_path)
        os.makedirs(log_dir, exist_ok=True)

        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    logger.propagate = False
    return logger


if __name__ == "__main__":
    logger = get_logger("test_logger")
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
