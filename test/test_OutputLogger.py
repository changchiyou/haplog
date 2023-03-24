import logging
import contextlib
from pathlib import Path

from logger_utils import instantiate_logger, OutputLogger

LOGGER_NAME = 'test'
MESSAGE = 'test'


def test_redirect(capsys):
    instantiate_logger(LOGGER_NAME, level_console=logging.DEBUG)
    with contextlib.redirect_stdout(
            OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)):    # type: ignore
        print(MESSAGE)

    captured = capsys.readouterr()
    assert f'DEBUG    {Path(__file__).name} - test_redirect() : {MESSAGE}' in captured.err


def test_redirect_info_level(capsys):
    instantiate_logger(LOGGER_NAME)
    with contextlib.redirect_stdout(
            OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)):    # type: ignore
        print(MESSAGE)

    captured = capsys.readouterr()
    assert f'DEBUG    {Path(__file__).name} - test_redirect() : {MESSAGE}' not in captured.err


def test_redirect_other_function(capsys):
    instantiate_logger(LOGGER_NAME, level_console=logging.DEBUG)

    def test():
        print(MESSAGE)

    with contextlib.redirect_stdout(
            OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)):    # type: ignore
        test()

    captured = capsys.readouterr()
    assert f'DEBUG    {Path(__file__).name} - test() : {MESSAGE}' in captured.err
