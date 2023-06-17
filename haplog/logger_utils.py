"""Some implements of `logging` enhancement."""
import logging
import multiprocessing
import platform
import queue
from logging import handlers
from pathlib import Path
from typing import Callable

LOGGING_FORMAT = (
    "%(asctime)s %(levelname)-8s [%(name)s] %(filename)s - %(funcName)s() : %(message)s"
)
BASE_LOG_NAME = "record"
SUFFIX_LOG_NAME = "%Y-%m-%d.log"


class CustomFormatter(logging.Formatter):
    """
    Custom log formatter class that inherits from `logging.Formatter`.
    It formats the log messages based on their log levels and applies color settings.
    """

    def __init__(self, costom_format: str):
        super().__init__()

        if platform.system() == "Windows":
            from colorama import init  # type: ignore

            init()

        # https://talyian.github.io/ansicolors/

        # black = "\x1b[30;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        green = "\x1b[32;20m"
        yellow = "\x1b[33;20m"
        # blue = "\x1b[34;20m"
        # magenta = "\x1b[35;20m"
        # cyan = "\x1b[36;20m"
        # white = "\x1b[37;20m"
        grey = "\x1b[38;20m"

        # \x1b[38;2;r;g;bm - foreground
        # \x1b[48;2;r;g;bm - background

        reset = "\x1b[0m"

        self.formats = {
            logging.DEBUG: grey + costom_format + reset,
            logging.INFO: green + costom_format + reset,
            logging.WARNING: yellow + costom_format + reset,
            logging.ERROR: red + costom_format + reset,
            logging.CRITICAL: bold_red + costom_format + reset,
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class OutputLogger:
    """
    serves as a pseudo file-like stream object that redirects written content to a logger instance.
    It overrides the `write` method to append the written messages to an internal buffer
    (`linebuf`). When a message ends with a newline character, it logs the buffered messages
    as a log record.
    """

    def __init__(self, logger_name: str, logging_level: int = logging.INFO) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logging_level = logging_level
        self.linebuf = ""

    def write(self, msg: str) -> None:
        r"""
        If redirected output end without `\n`, append it into `self.linebuf`,
        and log it out when the redirected output which end with `\n` comes.
        """
        self.linebuf += msg
        if msg.endswith("\n") is True:
            self.logger.log(
                self.logging_level,
                self.linebuf.rstrip(),
                stack_info=False,
                stacklevel=2,
            )
            self.linebuf = ""

    def flush(self) -> None:
        """
        Note that self.linebuf = '' is where the flush is being handled,
        rather than implementing a flush function.
        """


class MultiProcessLogger:
    """
    Implements a custom logger designed for multi-process environments.
    It is based on the 'Logging Cookbook - Logging to a single file from multiple processes' example
    in the Python documentation. It utilizes a multiprocessing queue and a listener process to
    enable logging across multiple processes. The class provides functionality for logging records
    to a file and printing logs to the console.
    """

    def __init__(
        self,
        # record logs into file
        log_path: str | Path | None = None,
        level_log: int = logging.DEBUG,
        format_log: str = LOGGING_FORMAT,
        base_log_name: str = BASE_LOG_NAME,
        suffix_log_name: str = SUFFIX_LOG_NAME,
        rotate_period: tuple[str, int] = ("midnight", 1),
        # print logs on console
        level_console: int = logging.INFO,
        format_console: str = LOGGING_FORMAT,
    ):
        self.log_path = log_path
        self.level_log = level_log
        self.format_log = format_log
        self.base_log_name = base_log_name
        self.suffix_log_name = suffix_log_name
        self.rotate_period = rotate_period
        self.level_console = level_console
        self.format_console = format_console

        self.queue = multiprocessing.Manager().Queue(-1)
        self.listener = multiprocessing.Process(
            target=self.listener_process, args=(self.queue, self.listener_configurer)
        )

    def listener_configurer(self):
        root = logging.getLogger()

        # logger for logs
        if self.log_path is not None:
            formatter_log = logging.Formatter(self.format_log)
            handler_log = handlers.TimedRotatingFileHandler(
                (Path(self.log_path) / self.base_log_name).resolve(),
                when=self.rotate_period[0],
                interval=self.rotate_period[1],
                encoding="utf-8",
            )
            handler_log.setFormatter(formatter_log)
            handler_log.suffix = self.suffix_log_name
            root.addHandler(handler_log)

        # logger for console
        handler_console = logging.StreamHandler()
        handler_console.setLevel(self.level_console)
        handler_console.setFormatter(CustomFormatter(self.format_console))
        root.addHandler(handler_console)

    def listener_process(self, _queue: queue.Queue, configurer: Callable) -> None:
        configurer()
        while True:
            try:
                record = _queue.get()
                if record is None:
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except BrokenPipeError:
                # https://github.com/changchiyou/haplog/issues/2
                self.join()
            except Exception:
                import sys
                import traceback

                print(
                    "Oops! An issue occurred during the logging process:",
                    file=sys.stderr,
                )
                traceback.print_exc(file=sys.stderr)

    def start(self):
        self.listener.start()

    def join(self):
        self.queue.put_nowait(None)
        self.listener.join()


def worker_configurer(_queue: queue.Queue, worker_level: int = logging.DEBUG) -> None:
    """
    Configure the logger for worker processes with input `_queue` handler.
    """
    handler = handlers.QueueHandler(_queue)
    root = logging.getLogger()
    root.addHandler(handler)
    # send all messages
    root.setLevel(worker_level)
