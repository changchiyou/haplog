"""Unit test for `haplog.OutputLogger` via `pytest`."""
import concurrent.futures
import contextlib
import logging
import multiprocessing
from pathlib import Path

from haplog import MultiProcessLogger, OutputLogger, worker_configurer

LOGGER_NAME = "test_logger"
MESSAGE = "test_info"
MULTI_PROCESS_NUM = 5

# pylint: disable=invalid-name


def test_redirect_debug_level(capfd):
    """Test the redirection of output from `print` to a logger with DEBUG level."""
    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)
    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):
        print(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_redirect_debug_level() : {MESSAGE}"
        in captured.err
    )


def func0(queue, configurer):
    """Redirect `print` message to logger which has `logging.DEBUG` level(for multi test only)."""
    configurer(queue)
    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):
        print(MESSAGE)


def test_multi_ing_debug_level(capfd):
    """
    (multi-process-ing)Test the redirection of output from `print` to a logger with DEBUG level.
    """
    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()

    workers = []
    for _ in range(MULTI_PROCESS_NUM):
        worker = multiprocessing.Process(
            target=func0, args=(mpl.queue, worker_configurer)
        )
        workers.append(worker)
        worker.start()
    for w in workers:
        w.join()

    mpl.join()

    captured = capfd.readouterr()

    assert (
        captured.err.count(
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {func0.__name__}() : {MESSAGE}"
        )
        == MULTI_PROCESS_NUM
    )


def test_multi_con_debug_level(capfd):
    """
    (multi-process-con)Test the redirection of output from `print` to a logger with DEBUG level.
    """
    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()

    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):
        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
            for _ in range(MULTI_PROCESS_NUM):
                executor.submit(func0, mpl.queue, worker_configurer)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        captured.err.count(
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {func0.__name__}() : {MESSAGE}"
        )
        == MULTI_PROCESS_NUM
    )


def test_redirect_info_level(capfd):
    """Test the redirection of output from `print` to a logger with default (INFO) level."""
    mpl = MultiProcessLogger()
    mpl.start()
    worker_configurer(mpl.queue)
    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):
        print(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_redirect() : {MESSAGE}"
        not in captured.err
    )


def test_redirect_other_function(capfd):
    """Test the redirection of output from other functions to a logger from another function."""

    def test1():
        print(MESSAGE)

    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)

    def test2():
        print(MESSAGE)

    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):
        test1()
        test2()

    mpl.join()

    captured = capfd.readouterr()
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test1() : {MESSAGE}"
        in captured.err
    )
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test2() : {MESSAGE}"
        in captured.err
    )
