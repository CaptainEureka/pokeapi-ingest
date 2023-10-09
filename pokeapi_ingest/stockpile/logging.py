import sys
import logging
from rich.console import Console
from rich.logging import RichHandler


def configure_logging() -> logging.Logger:
    console = Console()
    stdout_handler = RichHandler(level=logging.INFO, console=console)

    root_logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]")
    # Create and configure a handler for stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)

    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(stderr_handler)

    return root_logger
