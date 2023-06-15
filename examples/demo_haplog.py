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
    print(MESSAGE + " by third_party_function()")


def single_process():
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
    import time
    from random import random

    configurer(queue)

    name = multiprocessing.current_process().name
    logger = logging.getLogger(name)
    logger.info("Worker started: %s" % name)
    time.sleep(random())
    logger.info("Worker finished: %s" % name)


def multi_process():
    mpl = MultiProcessLogger(log_folder, level_console=logging.DEBUG)
    mpl.start()

    workers = []
    for _ in range(10):
        worker = multiprocessing.Process(
            target=worker_process, args=(mpl.queue, worker_configurer)
        )
        workers.append(worker)
        worker.start()
    for w in workers:
        w.join()

    mpl.join()


if __name__ == "__main__":
    single_process()
    multi_process()
