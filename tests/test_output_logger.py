"""Unit test for `haplog.OutputLogger` via `pytest`."""
import contextlib
import logging
from pathlib import Path

from haplog import MultiProcessLogger, OutputLogger, worker_configurer

LOGGER_NAME = "test"
MESSAGE = "test"


def test_redirect_debug_level(capfd):
    """Test the redirection of output to a logger with DEBUG level."""
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


def test_redirect_info_level(capfd):
    """Test the redirection of output to a logger with default (INFO) level."""
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
    """Test the redirection of output to a logger from another function."""

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
