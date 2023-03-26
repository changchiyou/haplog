from setuptools import setup, find_packages

requirements = ['colorama']

setup(
    name='haplog',
    version='0.0.0',
    author='changchiyou',
    url='https://github.com/changchiyou/haplog',
    description='Some utilities to enhance the experience of using the logging module',
    # PEP 604 – Allow writing union types as X | Y
    python_requires='>=3.10',
    install_requires=requirements,
    packages=find_packages(exclude=('.vscode', 'tests', 'examples')),
)