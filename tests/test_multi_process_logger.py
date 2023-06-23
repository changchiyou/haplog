"""Unit test for `haplog.MultiProcessLogger` via `pytest`."""
import concurrent.futures
import logging
import multiprocessing
from pathlib import Path

from haplog import BASE_LOG_NAME, MultiProcessLogger, worker_configurer

# pylint: disable=invalid-name

# TODO: rearrangement these local varaibles, classes, and functions,
# which are designed for test function.
LOGGER_NAME = "test_logger"
INFO_MESSAGE = "test_info"
DEBUG_MESSAGE = "test_debug"
WARNING_MESSAGE = "test_warning"
MULTI_PROCESS_NUM = 5


class LogListner:
    """Implement for test quickly only."""

    def __init__(self, **kwargs):
        self.mpl = MultiProcessLogger(**kwargs)
        self.start()

    def start(self):
        """Start log-listner."""
        self.mpl.start()

    def stop(self):
        """Stop log-listner."""
        self.mpl.join()


class SingleProcess(LogListner):
    """Implement a log-listner for single-process."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, function):
        """Execute function with `self.logger`."""
        function(self.mpl.queue, worker_configurer)
        self.stop()


class MultiProcessMultiprocessing(LogListner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, function, num: int):
        """Execute function with `self.logger`."""
        workers = []
        for _ in range(num):
            worker = multiprocessing.Process(
                target=function, args=(self.mpl.queue, worker_configurer)
            )
            workers.append(worker)
            worker.start()
        for w in workers:
            w.join()
        self.stop()


class MultiProcessConcurrentFutures(LogListner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, function, num: int):
        """Execute function with `self.logger`."""
        with concurrent.futures.ProcessPoolExecutor(max_workers=num) as executor:
            for _ in range(num):
                executor.submit(function, self.mpl.queue, worker_configurer)


def logs_info_1(queue, configurer):
    configurer(queue)

    logger = logging.getLogger(LOGGER_NAME)
    logger.info(INFO_MESSAGE)


def logs_debug_1(queue, configurer):
    configurer(queue)

    logger = logging.getLogger(LOGGER_NAME)
    logger.debug(DEBUG_MESSAGE)


def logs_warning_1(queue, configurer):
    configurer(queue)

    logger = logging.getLogger(LOGGER_NAME)
    logger.warning(WARNING_MESSAGE)


def logs_info_1_debug_1(queue, configurer):
    configurer(queue)

    logger = logging.getLogger(LOGGER_NAME)
    logger.info(INFO_MESSAGE)
    logger.debug(DEBUG_MESSAGE)


# naming rule:
# test_[single/multi_[{multi_way}]][_console_{level_console}][_log_{level_log}][_{logger_log}]*
#
# e.g. test_single_console_default_info() means: single process, console, default level, logger.info


def test_single_console_default_info(capfd):
    """
    (Single-process)Test the console logging based on default level (INFO) set
    with single `logger.info()`. Should appear in console.
    """
    single_process = SingleProcess()

    single_process.execute(logs_info_1)

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {logs_info_1.__name__}() : {INFO_MESSAGE}" in captured.err
    )


def test_single_console_default_debug(capfd):
    """
    (Single-process)Test the console logging based on default level (INFO) set
    with single `logger.debug()`. Should not appear anything in console.
    """
    single_process = SingleProcess()

    single_process.execute(logs_debug_1)

    captured = capfd.readouterr()

    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {logs_debug_1.__name__}() : {DEBUG_MESSAGE}" not in captured.err
    )


def test_single_console_default_warning(capfd):
    """
    (Single-process)Test the console logging based on default level (INFO) set
    with single `logger.warning()`. Should appear in console.
    """
    single_process = SingleProcess()

    single_process.execute(logs_warning_1)

    captured = capfd.readouterr()

    assert (
        f"WARNING  [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {logs_warning_1.__name__}() : {WARNING_MESSAGE}" in captured.err
    )


def test_multi_ing_console_default_info(capfd):
    """
    (Multi-process-ing)Test the console logging based on default level (INFO) set
    with single`logger.info()`. Should appear in console.
    """
    multi_process_multiprocessing = MultiProcessMultiprocessing()

    multi_process_multiprocessing.execute(logs_info_1, MULTI_PROCESS_NUM)

    captured = capfd.readouterr()

    assert (
        captured.err.count(
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1.__name__}() : {INFO_MESSAGE}"
        )
        == MULTI_PROCESS_NUM
    )


def test_multi_con_console_default_info(capfd):
    """(Multi-process-con)Test the console logging based on default level (INFO) set
    with single`logger.info()`. Should appear in console.
    """
    multi_process_concurrent_futures = MultiProcessConcurrentFutures()

    multi_process_concurrent_futures.execute(logs_info_1, MULTI_PROCESS_NUM)

    captured = capfd.readouterr()

    assert (
        captured.err.count(
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1.__name__}() : {INFO_MESSAGE}"
        )
        == MULTI_PROCESS_NUM
    )


def test_single_console_info_info(capfd):
    """
    (Single-process)Test the console logging based on explicit level (`logging.INFO`) set
    with single `logger.info()`. Should appear in console.
    """
    single_process = SingleProcess(level_console=logging.INFO)

    single_process.execute(logs_info_1)

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {logs_info_1.__name__}() : {INFO_MESSAGE}" in captured.err
    )


def test_single_console_debug_debug(capfd):
    """
    (Single-process)Test the console logging based on `logging.DEBUG` set
    with single `logger.info()`. Should appear in console.
    """
    single_process = SingleProcess(level_console=logging.DEBUG)

    single_process.execute(logs_debug_1)

    captured = capfd.readouterr()

    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {logs_debug_1.__name__}() : {DEBUG_MESSAGE}" in captured.err
    )


def test_single_console_default_debug_info(capfd):
    """
    (Single-process)Test the console logging based on default level `logging.info` set
    with `logger.info()` and `logger.debug`. Should only appear info message in console.
    """
    single_process = SingleProcess()

    single_process.execute(logs_info_1_debug_1)

    captured = capfd.readouterr()

    assert (
        f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}" in captured.err
    )
    assert (
        f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
        f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}" not in captured.err
    )


def test_single_console_debug_log_debug_info_debug(tmp_path, capfd):
    """
    (Single-process)Test writing logs to a log file based on both logs/console `logging.DEBUG`,
    should appear ALL message from logger because `logging.DEBUG` doesn't filt any
    message in default.
    """
    single_process = SingleProcess(log_path=tmp_path, level_console=logging.DEBUG)

    single_process.execute(logs_info_1_debug_1)

    with open(tmp_path / BASE_LOG_NAME, mode="r", encoding="utf-8") as log_file:
        contents = log_file.read()
        log_file.close()

        captured = capfd.readouterr()

        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}" in captured.err
        )
        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}" in captured.err
        )

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}" in contents
        )
        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}" in contents
        )


def test_single_console_info_log_debug_info_debug(tmp_path, capfd):
    """
    (Single-process)Test the project's ability to filter out messages based on `logging.INFO`
    logging console levels and `logging.DEBUG` logs level with both DEBUG and INFO level logger,
    should only appear INFO's message in console but contain both messages from DEBUG and INFO
    level logger in log file.
    """
    single_process = SingleProcess(
        log_path=tmp_path, level_console=logging.INFO, level_log=logging.DEBUG
    )

    single_process.execute(logs_info_1_debug_1)

    with open(tmp_path / BASE_LOG_NAME, mode="r", encoding="utf-8") as log_file:
        contents = log_file.read()
        log_file.close()

        captured = capfd.readouterr()

        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}" not in captured.err
        )
        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}" in captured.err
        )

        assert (
            f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}" in contents
        )
        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}" in contents
        )


def test_multi_ing_console_info_log_debug_info_debug(tmp_path, capfd):
    """
    (Multi-process-ing)Test the project's ability to filter out messages based on `logging.INFO`
    logging console levels and `logging.DEBUG` logs level with both DEBUG and INFO level logger,
    should only appear INFO's message in console but contain both messages from DEBUG and INFO
    level logger in log file.
    """
    multi_process_multiprocessing = MultiProcessMultiprocessing(
        log_path=tmp_path, level_console=logging.INFO, level_log=logging.DEBUG
    )

    multi_process_multiprocessing.execute(logs_info_1_debug_1, MULTI_PROCESS_NUM)

    with open(tmp_path / BASE_LOG_NAME, mode="r", encoding="utf-8") as log_file:
        contents = log_file.read()
        log_file.close()

        captured = capfd.readouterr()

        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}" not in captured.err
        )
        assert (
            captured.err.count(
                f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
                f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}"
            )
            == MULTI_PROCESS_NUM
        )

        assert (
            contents.count(
                f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
                f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}"
            )
            == MULTI_PROCESS_NUM
        )
        assert (
            contents.count(
                f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
                f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}"
            )
            == MULTI_PROCESS_NUM
        )


def test_multi_con_console_info_log_debug_info_debug(tmp_path, capfd):
    """
    (Multi-process-con)Test the project's ability to filter out messages based on `logging.INFO`
    logging console levels and `logging.DEBUG` logs level with both DEBUG and INFO level logger,
    should only appear INFO's message in console but contain both messages from DEBUG and INFO
    level logger in log file.
    """
    multi_process_concurrent_futures = MultiProcessConcurrentFutures(
        log_path=tmp_path, level_console=logging.INFO, level_log=logging.DEBUG
    )

    multi_process_concurrent_futures.execute(logs_info_1_debug_1, MULTI_PROCESS_NUM)

    with open(tmp_path / BASE_LOG_NAME, mode="r", encoding="utf-8") as log_file:
        contents = log_file.read()
        log_file.close()

        captured = capfd.readouterr()

        assert (
            f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
            f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}" not in captured.err
        )
        assert (
            captured.err.count(
                f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
                f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}"
            )
            == MULTI_PROCESS_NUM
        )

        assert (
            contents.count(
                f"INFO     [{LOGGER_NAME}] {Path(__file__).name}"
                f" - {logs_info_1_debug_1.__name__}() : {INFO_MESSAGE}"
            )
            == MULTI_PROCESS_NUM
        )
        assert (
            contents.count(
                f"DEBUG    [{LOGGER_NAME}] {Path(__file__).name}"
                f" - {logs_info_1_debug_1.__name__}() : {DEBUG_MESSAGE}"
            )
            == MULTI_PROCESS_NUM
        )
