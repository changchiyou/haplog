"""Unit test for `haplog.MultiProcessLogger` via `pytest`."""
import inspect
import logging
from pathlib import Path

from haplog import BASE_LOG_NAME, MultiProcessLogger, worker_configurer

# https://stackoverflow.com/questions/76487303/pytest-unit-test-for-loggingmulti-processqueuehandler
# May be useful: https://github.com/pytest-dev/pytest/issues/3037#issuecomment-745050393

LOGGER_NAME = "test_logger"
MESSAGE = "test_info"

# pylint: disable=invalid-name


def test_console_default_info_single_process(capfd):
    """(Single-process)Test the console logging with default level (INFO)."""
    mpl = MultiProcessLogger()
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
    )


def test_console_default_info_multi_process_normal(capfd):
    """(Multi-process)Test the console logging with default level (INFO)."""
    mpl = MultiProcessLogger()
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
    )


def test_console_default_info_multi_process_(capfd):
    """(Multi-process)Test the console logging with default level (INFO)."""
    mpl = MultiProcessLogger()
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
    )


def test_console_info_single_process(capfd):
    """(Single-process)Test the console logging with explicit INFO level."""
    mpl = MultiProcessLogger(level_console=logging.INFO)
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
    )


def test_console_debug_single_process(capfd):
    """(Single-process)Test the console logging with DEBUG level."""
    mpl = MultiProcessLogger(level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.debug(MESSAGE)

    mpl.join()

    captured = capfd.readouterr()

    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
    )


def test_console_debug_info_level_single_process(capfd):
    """
    (Single-process)Test the project's ability to filter out messages based on `logging.INFO`
    logging console levels with both DEBUG and INFO level logger, should only appear INFO's
    message in console.
    """
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
        f" - {inspect.stack()[0][3]}() : {MESSAGE}" not in captured.err
    )
    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
    )


def test_log_single_process(tmp_path, capfd):
    """
    (Single-process)Test writing logs to a log file based on both logs/console `logging.DEBUG`,
    should appear ALL message from logger because `logging.DEBUG` doesn't filt any
    message in default.
    """
    mpl = MultiProcessLogger(log_path=tmp_path, level_console=logging.DEBUG)
    mpl.start()
    worker_configurer(mpl.queue)

    logger = logging.getLogger(LOGGER_NAME)

    logger.info(MESSAGE)
    logger.debug(MESSAGE)

    mpl.join()

    with open(tmp_path / BASE_LOG_NAME, mode="r", encoding="utf-8") as log_file:
        contents = log_file.read()
        log_file.close()

        captured = capfd.readouterr()

        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
        )
        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
        )

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" in contents
        )
        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" in contents
        )


def test_console_log_diff_level_single_process(tmp_path, capfd):
    """
    (Single-process)Test the project's ability to filter out messages based on `logging.INFO`
    logging console levels and `logging.DEBUG` logs level with both DEBUG and INFO level logger,
    should only appear INFO's message in console but contain both messages from DEBUG and INFO
    level logger in log file.
    """
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

    with open(tmp_path / BASE_LOG_NAME, mode="r", encoding="utf-8") as log_file:
        contents = log_file.read()
        log_file.close()

        captured = capfd.readouterr()

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" in captured.err
        )
        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" not in captured.err
        )

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" in contents
        )
        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {inspect.stack()[0][3]}() : {MESSAGE}" in contents
        )
