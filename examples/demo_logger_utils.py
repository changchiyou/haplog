import logging
from pathlib import Path
from contextlib import redirect_stdout
from logger_utils import instantiate_logger, OutputLogger

LOGGER_NAME = 'test'
MESSAGE = 'test'


def third_party_function():
    print(MESSAGE + ' by third_party_function()')


def test():
    log_folder = ((Path(__file__).parent) / 'logs')

    if log_folder.exists() is False:
        log_folder.mkdir()

    instantiate_logger(LOGGER_NAME, log_folder, level_console=logging.DEBUG)
    logger = logging.getLogger(LOGGER_NAME)

    with redirect_stdout(OutputLogger(logger_name=LOGGER_NAME,
                                      logging_level=logging.DEBUG)):    # type: ignore
        print(MESSAGE + ' by print()')
        third_party_function()

    logger.debug(MESSAGE)
    logger.info(MESSAGE)
    logger.warning(MESSAGE)
    logger.error(MESSAGE)
    logger.critical(MESSAGE)


if __name__ == '__main__':
    test()