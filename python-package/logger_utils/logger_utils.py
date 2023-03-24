"""Some implements of `logging` enhancement"""
import logging
from logging import handlers
from pathlib import Path

LOGGING_FORMAT = "%(asctime)s %(levelname)-8s %(filename)s - %(funcName)s() : %(message)s"
BASE_LOG_NAME = 'record'
SUFFIX_LOG_NAME = '%Y-%m-%d.log'


class CustomFormatter(logging.Formatter):
    """For `StreamHandler.setFormatter`"""

    def __init__(self, costom_format: str):

        super().__init__()

        # https://talyian.github.io/ansicolors/

        #black = "\x1b[30;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        green = "\x1b[32;20m"
        yellow = "\x1b[33;20m"
        #blue = "\x1b[34;20m"
        #magenta = "\x1b[35;20m"
        #cyan = "\x1b[36;20m"
        #white = "\x1b[37;20m"
        grey = "\x1b[38;20m"

        # \x1b[38;2;r;g;bm - foreground
        # \x1b[48;2;r;g;bm - background

        reset = "\x1b[0m"

        self.formats = {
            logging.DEBUG: grey + costom_format + reset,
            logging.INFO: green + costom_format + reset,
            logging.WARNING: yellow + costom_format + reset,
            logging.ERROR: red + costom_format + reset,
            logging.CRITICAL: bold_red + costom_format + reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def instantiate_logger(
    logger_name: str,
    # record logs into file
    log_path: str | Path | None = None,
    level_log: int = logging.DEBUG,
    format_log: str = LOGGING_FORMAT,
    base_log_name: str = BASE_LOG_NAME,
    suffix_log_name: str = SUFFIX_LOG_NAME,
    rotate_period: tuple[str, int] = ('midnight', 1),
    # print logs on console
    level_console: int = logging.INFO,
    format_console: str = LOGGING_FORMAT,
) -> None:
    """
    Make logging method can both show message on console and record on file.

    If the value of arg `log_path` is `None` (default), then the logs would not be recorded.
    """

    # create a new logger for customization
    logger = logging.getLogger(logger_name)
    logger.setLevel(level_log)

    # logger for log
    if log_path is not None:
        formatter_log = logging.Formatter(format_log)
        handler_log = handlers.TimedRotatingFileHandler((Path(log_path) / base_log_name).resolve(),
                                                        when=rotate_period[0],
                                                        interval=rotate_period[1])
        handler_log.setFormatter(formatter_log)
        handler_log.suffix = suffix_log_name
        logger.addHandler(handler_log)

    # logger for console
    handler_console = logging.StreamHandler()
    handler_console.setLevel(level_console)
    handler_console.setFormatter(CustomFormatter(format_console))
    logger.addHandler(handler_console)


class OutputLogger():
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger_name: str, logging_level: int = logging.INFO) -> None:
        """
        Get logger with specific `name` and going to log info with `level` level.
        """
        self.logger = logging.getLogger(logger_name)
        self.logging_level = logging_level
        self.linebuf = ''

    def write(self, msg: str) -> None:
        """
        If redirected output end without `\\n`, append it into `self.linebuf`,
        and log it out when the redirected output which end with '\n' comes.
        """
        self.linebuf += msg
        if msg.endswith('\n') is True:
            self.logger.log(self.logging_level,
                            self.linebuf.rstrip(),
                            stack_info=False,
                            stacklevel=2)
            self.linebuf = ''

    def flush(self) -> None:
        """
        Note that self.linebuf = '' is where the flush is being handled, 
        rather than implementing a flush function.
        """
