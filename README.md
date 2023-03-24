# [Introdoction](#content)
Some utilities to enhance the experience of using the `logging` module:

1. `(function) instantiate_logger`
   Instantiate the logger so that it can display colored text in the console, and create a new log every day and record messages in it.
2. `(class) OutputLogger`
   Redirect the standard output of third-party modules to log records, which is usually used when developers are unwilling to spend time manually changing `print()` to the corresponding `logging` function.

# [Content](#content)
- [Introdoction](#introdoction)
- [Content](#content)
- [Installation](#installation)
- [Usage](#usage)
- [Visual Effect](#visual-effect)
- [Reference](#reference)

# [Installation](#content)
```
pip install "git+https://github.com/changchiyou/logger_utils.git#egg=logger_utils\&subdirectory=python-package"
```

# [Usage](#content)
## [(function) instantiate_logger](#content)
1. Execute first:
    ```
    instantiate_logger('your_logger_name')
    ```
2. Then get the logger before you want to log some info:
    ```
    logger = logging.getLogger('your_logger_name)

    logger.debug('debug msg')
    logger.info('info msg')
    logger.warning('warning msg')
    logger.error('error msg')
    logger.critical('critical msg')
    ```
3. If you want the messages to be logged to the log instead of just displayed on the console. Go back to step `1.` and add another argument:
    ```
    instantiate_logger('your_logger_name', 'your_logs_folder_path')
    ```
    The messages will first be recorded in `log`, and after the date is changed every day, the date of the previous day will be added as a suffix after the file name, such as `log.20230324`, and a new `log` file will be created to continue recording messages. The folder structure is as follows:
    ```
    your_logs_folder_path
    ├── log
    ├── log.20230324
    ├── log.20230323
    ├── log.20230322
    └── log.20230321
    ```

## [(class) OutputLogger](#content)
Use the `with` syntax to wrap the content you want to redirect:
```
from contextlib import redirect_stdout

instantiate_logger(LOGGER_NAME)

with redirect_stdout(OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)):
    print(MESSAGE)
    third_party_function_has_print()
```

# [Visual Effect](#content)

Download and execute [`/examples/demo_logger_utils.py`](/examples/demo_logger_utils.py):

![image](https://i.imgur.com/fEOZr2e.png)

Check [ANSI Color Codes](https://talyian.github.io/ansicolors/) for more personalized color schemes.

# [Reference](#content)
- [StackOverflow: How to redirect stdout and stderr to logger in Python](https://stackoverflow.com/a/31688396)
- [StackOverflow: How can I color Python logging output?](https://stackoverflow.com/a/56944256)
