import logging


# Configure root (global) logging once (console only; no file)
def setup_logging(level: int = logging.INFO) -> None:
    """Set up basic logging configuration for the entire app."""
    logging.basicConfig(
        level=level,
        # filename="logs/app.log",
        format="LOG: %(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
    )


# Get a module specific logger
def get_logger(name: str) -> logging.Logger:
    """Returns a logger with the given module name."""
    return logging.getLogger(name)
