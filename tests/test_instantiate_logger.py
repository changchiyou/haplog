import logging
from pathlib import Path

from logger_utils import instantiate_logger

LOGGER_NAME = 'test'
MESSAGE = 'test'


def test_console_info(capsys):
    instantiate_logger(LOGGER_NAME)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)

    captured = capsys.readouterr()

    assert f'INFO     {Path(__file__).name} - test_console_info() : {MESSAGE}' in captured.err


def test_console_debug(capsys):
    instantiate_logger(LOGGER_NAME, level_console=logging.DEBUG)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug(MESSAGE)

    captured = capsys.readouterr()

    assert f'DEBUG    {Path(__file__).name} - test_console_debug() : {MESSAGE}' in captured.err


def test_console_debug_info_level(capsys):
    instantiate_logger(LOGGER_NAME)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug(MESSAGE)

    captured = capsys.readouterr()

    assert f'DEBUG    {Path(__file__).name} - test_console_debug() : {MESSAGE}' not in captured.err


def test_log(tmp_path, capsys):
    instantiate_logger(LOGGER_NAME, tmp_path)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)
    logger.debug(MESSAGE)

    captured = capsys.readouterr()

    assert f'INFO     {Path(__file__).name} - test_log() : {MESSAGE}' in captured.err
    assert f'DEBUG    {Path(__file__).name} - test_log() : {MESSAGE}' not in captured.err

    File = open(tmp_path / 'record', mode='r')
    contents = File.read()
    File.close()

    assert f'INFO     {Path(__file__).name} - test_log() : {MESSAGE}' in contents
    assert f'DEBUG    {Path(__file__).name} - test_log() : {MESSAGE}' in contents