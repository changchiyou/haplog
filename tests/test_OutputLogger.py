import contextlib
import logging
from pathlib import Path

from haplog import MultiProcessLogger, OutputLogger, worker_configurer

LOGGER_NAME = "test"
MESSAGE = "test"


def test_redirect(capfd):
    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)
    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):  # type: ignore
        print(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_redirect() : {MESSAGE}"
        in captured.err
    )


def test_redirect_info_level(capfd):
    mpl = MultiProcessLogger()
    mpl.start()
    worker_configurer(mpl.queue)
    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):  # type: ignore
        print(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_redirect() : {MESSAGE}"
        not in captured.err
    )


def test_redirect_other_function(capfd):
    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)

    def test():
        print(MESSAGE)

    with contextlib.redirect_stdout(
        OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)  # type: ignore
    ):  # type: ignore
        test()

    mpl.join()

    captured = capfd.readouterr()
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test() : {MESSAGE}"
        in captured.err
    )
