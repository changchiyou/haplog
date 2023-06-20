"""Demo for haplog, including single/multi-process and redirecting msg to logger."""
import concurrent.futures
import logging
import logging.handlers
import multiprocessing
from contextlib import redirect_stdout
from pathlib import Path

from haplog import MultiProcessLogger, OutputLogger, worker_configurer

LOGGER_NAME = "test"
MESSAGE = "test"

log_folder = (Path(__file__).parent) / "logs"

if log_folder.exists() is False:
    log_folder.mkdir()


def third_party_function():
    """Third-party function for `OutputLogger` redirecting showcase."""
    print(MESSAGE + " by third_party_function()")


def single_process():
    """Single process contains `OutputLogger` for redirecting."""
    mpl = MultiProcessLogger(log_folder, level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    with redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):
        print(MESSAGE + " by print()")
        third_party_function()

    logger.debug(MESSAGE)
    logger.info(MESSAGE)
    logger.warning(MESSAGE)
    logger.error(MESSAGE)
    logger.critical(MESSAGE)

    mpl.join()


def worker_process(queue, configurer):
    """Estimate the function of multi-process."""
    # pylint: disable-next=import-outside-toplevel
    import time

    # pylint: disable-next=import-outside-toplevel
    from random import random

    configurer(queue)

    name = multiprocessing.current_process().name
    logger = logging.getLogger(name)
    logger.info("Worker started: %s", name)
    time.sleep(random())
    logger.info("Worker finished: %s", name)


def multi_process():
    """Multi-process use `concurrent.futures.ProcessPoolExecutor`."""
    mpl = MultiProcessLogger(log_folder, level_console=logging.DEBUG)
    mpl.start()

    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for _ in range(10):
            executor.submit(worker_process, mpl.queue, worker_configurer)

    mpl.join()


if __name__ == "__main__":
    single_process()
    multi_process()
