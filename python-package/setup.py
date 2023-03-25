from setuptools import setup, find_packages

requirements = ['colorama']

setup(
    name='logger_utils',
    version='0.0.0',
    author='changchiyou',
    url='https://github.com/changchiyou/logger_utils',
    description='',
    # PEP 604 – Allow writing union types as X | Y
    python_requires='>=3.10',
    install_requires=requirements,
    packages=find_packages(),
)