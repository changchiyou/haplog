"""Unit test for `haplog.MultiProcessLogger` via `pytest`."""
import logging
from pathlib import Path

from haplog import BASE_LOG_NAME, MultiProcessLogger, worker_configurer

# https://stackoverflow.com/questions/76487303/pytest-unit-test-for-loggingmulti-processqueuehandler
# May be useful: https://github.com/pytest-dev/pytest/issues/3037#issuecomment-745050393

LOGGER_NAME = "test"
MESSAGE = "test"


def test_console_default_info(capfd):
    """Test the console logging with default level (INFO)."""
    mpl = MultiProcessLogger()
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name} - test_console_default_info() : {MESSAGE}"
        in captured.err
    )


def test_console_info(capfd):
    """Test the console logging with explicit INFO level."""
    mpl = MultiProcessLogger(level_console=logging.INFO)
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name} - test_console_info() : {MESSAGE}"
        in captured.err
    )


def test_console_debug(capfd):
    """Test the console logging with DEBUG level."""
    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.debug(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_console_debug() : {MESSAGE}"
        in captured.err
    )


def test_console_debug_info_level(capfd):
    """Test the console logging with default level (INFO) but log with DEBUG and INFO level."""
    mpl = MultiProcessLogger()
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.debug(MESSAGE)
    logger.info(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
        f" - test_console_debug_info_level() : {MESSAGE}" not in captured.err
    )
    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - test_console_debug_info_level() : {MESSAGE}" in captured.err
    )


def test_log(tmp_path, capfd):
    """Test writing logs to a log file with both DEBUG level."""
    mpl = MultiProcessLogger(log_path=tmp_path, level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)
    logger.debug(MESSAGE)

    mpl.join()

    with open(tmp_path / BASE_LOG_NAME, mode="r") as File:
        contents = File.read()
        File.close()

        captured = capfd.readouterr()

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name} - test_log() : {MESSAGE}"
            in captured.err
        )

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name} - test_log() : {MESSAGE}"
            in contents
        )
        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_log() : {MESSAGE}"
            in contents
        )


def test_console_log_diff_level(tmp_path, capfd):
    """Test console logging and log file writing with different levels."""
    mpl = MultiProcessLogger(
        log_path=tmp_path,
        # default
        level_console=logging.INFO,
        level_log=logging.DEBUG,
    )
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)
    logger.debug(MESSAGE)

    mpl.join()

    with open(tmp_path / BASE_LOG_NAME, mode="r") as File:
        contents = File.read()
        File.close()

        captured = capfd.readouterr()

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name} - test_console_log_diff_level() : {MESSAGE}"
            in captured.err
        )

        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_console_log_diff_level() : {MESSAGE}"
            not in captured.err
        )

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name} - test_console_log_diff_level() : {MESSAGE}"
            in contents
        )
        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name} - test_console_log_diff_level() : {MESSAGE}"
            not in contents
        )
