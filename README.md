# haplog

Happy logging guys :)

## [Introdoction](#content)

Some utilities to enhance the experience of using the `logging` module:

1. `(function) instantiate_logger`
   Instantiate the logger so that it can display colored text in the console, and create a new log every day and record messages in it.
2. `(class) OutputLogger`
   Redirect the standard output of third-party modules to log records, which is usually used when developers are unwilling to spend time manually changing `print()` to the corresponding `logging` function.

## [Content](#content)

- [Introdoction](#introdoction)
- [Content](#content)
- [Installation](#installation)
- [Usage](#usage)
- [Visual Effect](#visual-effect)
- [Reference](#reference)

## [Installation](#content)

```console
pip install "https://github.com/changchiyou/haplog/archive/main.zip"
```

## [Usage](#content)

### [(function) instantiate_logger](#content)

1. Execute first:
   ```python
   instantiate_logger('your_logger_name')
   ```
2. Then get the logger before you want to log some info:

   ```python
   logger = logging.getLogger('your_logger_name')

   logger.debug('debug msg')
   logger.info('info msg')
   logger.warning('warning msg')
   logger.error('error msg')
   logger.critical('critical msg')
   ```

3. If you want the messages to be logged to the log instead of just displayed on the console. Go back to step `1.` and add another argument:
   ```python
   instantiate_logger('your_logger_name', 'your_logs_folder_path')
   ```
   The messages will first be recorded in `record`, and after the date is changed every day, the date of the previous day will be added as a suffix after the file name, such as `record.2023-03-24.log`, and a new `record` file will be created to continue recording messages. The folder structure is as follows:
   ```
   your_logs_folder_path
   ├── record
   ├── record.2023-03-24.log
   ├── record.2023-03-23.log
   ├── record.2023-03-22.log
   └── record.2023-03-21.log
   ```

### [(class) OutputLogger](#content)

Use the `with` syntax to wrap the content you want to redirect:

```python
from contextlib import redirect_stdout

instantiate_logger(LOGGER_NAME)

with redirect_stdout(OutputLogger(logger_name=LOGGER_NAME, logging_level=logging.DEBUG)):
    print(MESSAGE)
    third_party_function_has_print()
```

## [Visual Effect](#content)

Download and execute [`/examples/demo_haplog.py`](/examples/demo_haplog.py):

![image](https://i.imgur.com/jQgP93Y.png)

Check [ANSI Color Codes](https://talyian.github.io/ansicolors/) for more personalized color schemes.

## [Reference](#content)

- [StackOverflow: How to redirect stdout and stderr to logger in Python](https://stackoverflow.com/a/31688396)
- [StackOverflow: How can I color Python logging output?](https://stackoverflow.com/a/56944256)
- [Delgan/loguru: Python logging made (stupidly) simple - GitHub](https://github.com/Delgan/loguru)
- [Logging Cookbook - Logging to a single file from multiple processes](https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes:~:text=Although%20logging%20is%20thread%2Dsafe%2C%20and%20logging%20to%20a%20single%20file%20from%20multiple%20threads%20in%20a%20single%20process%20is%20supported%2C%20logging%20to%20a%20single%20file%20from%20multiple%20processes%20is%20not%20supported%2C%20because%20there%20is%20no%20standard%20way%20to%20serialize%20access%20to%20a%20single%20file%20across%20multiple%20processes%20in%20Python)
- [Started multiprocessing.Process instances are unserialisable #91090](https://github.com/python/cpython/issues/91090)
- [gh-91090: Make started multiprocessing.Process instances and started multiprocessing.managers.BaseManager instances serialisable #31701](https://github.com/python/cpython/pull/31701)
