import logging
from pathlib import Path


# Configure root (global) logging once (console only; no file)
def setup_logging(level: int = logging.INFO) -> None:
    """
    Set up basic logging configuration for the entire app.

    Set up logging to file + console.
    """

    # NOTE: go to the proejct's root dir from this file (test manually)
    root_dir = Path(__file__).resolve().parent.parent

    # Create /logs/ folder at root
    log_dir = root_dir / "logs"  # gitignore files in it `logs/`
    log_dir.mkdir(exist_ok=True)  # create dir if doesn't already exists

    # Create app.log file
    log_file = log_dir / "app.log"
    # this not necessary -> FileHanlder creates the file automatically
    log_file.touch(exist_ok=True)  # create file if doesn't already exists

    log_format = "LOG: %(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s"

    # FileHandler() automatically creates the log_file if it doesn't already exists
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(log_format))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers (b/c of implicit "uvicorn --reload")
    root_logger.handlers.clear()  # safe from `uvicorn --reload`

    # Add all handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


# Get a module specific logger
def get_logger(name: str) -> logging.Logger:
    """Returns a logger with the given module name."""
    return logging.getLogger(name)
