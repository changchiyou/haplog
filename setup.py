from setuptools import setup

requirements = ["colorama>=0.3.4 ; platform_system=='Windows'"]

setup(
    name="haplog",
    packages=["haplog"],
    version="1.0.0",
    author="changchiyou",
    url="https://github.com/changchiyou/haplog",
    keywords=["haplog", "logging", "logger", "log"],
    license="MIT license",
    description="Some utilities to enhance the experience of using the logging module",
    # PEP 604 – Allow writing union types as X | Y
    python_requires=">=3.10",
    install_requires=requirements,
)
