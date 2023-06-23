# haplog

Happy logging guys :)

## Content

- [Introdoction](#introdoction)
- [Installation](#installation)
- [Usage & Visual Effect](#usage--visual-effect)
- [Reference](#reference)

## [Introdoction](#content)

Provides enhancements for `logging` functionality, including:

1. Color the texts of `logging`:
   https://github.com/changchiyou/haplog/blob/314615619d2b3b338a39025d86fb13992e4d32d6/haplog/logger_utils.py#L30-L54
2. Redirect the standard output of third-party modules to log records, which is usually used when developers are unwilling to spend time manually changing `print()` to the corresponding `logging` function.
   https://github.com/changchiyou/haplog/blob/314615619d2b3b338a39025d86fb13992e4d32d6/haplog/logger_utils.py#L62-L68
   https://github.com/changchiyou/haplog/blob/314615619d2b3b338a39025d86fb13992e4d32d6/examples/demo_haplog.py#L30-L34
3. Logging (of cource):
   https://github.com/changchiyou/haplog/blob/314615619d2b3b338a39025d86fb13992e4d32d6/haplog/logger_utils.py#L97-L104
   1. single-process:
      https://github.com/changchiyou/haplog/blob/314615619d2b3b338a39025d86fb13992e4d32d6/examples/demo_haplog.py#L23-L42
   2. multi-process:
      https://github.com/changchiyou/haplog/blob/314615619d2b3b338a39025d86fb13992e4d32d6/examples/demo_haplog.py#L58-L66

## [Installation](#content)

```console
pip install "https://github.com/changchiyou/haplog/archive/main.zip"
```

## [Usage & Visual Effect](#content)

Download and execute [`/examples/demo_haplog.py`](/examples/demo_haplog.py):

https://github.com/changchiyou/haplog/blob/314615619d2b3b338a39025d86fb13992e4d32d6/examples/demo_haplog.py#L1-L71

![image](https://i.imgur.com/flpVeXN.png)

Check [ANSI Color Codes](https://talyian.github.io/ansicolors/) for more personalized color schemes.

## [Reference](#content)

- [StackOverflow: How to redirect stdout and stderr to logger in Python](https://stackoverflow.com/a/31688396)
- [StackOverflow: How can I color Python logging output?](https://stackoverflow.com/a/56944256)
- [Delgan/loguru: Python logging made (stupidly) simple - GitHub](https://github.com/Delgan/loguru)
- [Logging Cookbook - Logging to a single file from multiple processes](https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes)
- https://github.com/python/cpython/issues/91090
- https://github.com/python/cpython/pull/31701
