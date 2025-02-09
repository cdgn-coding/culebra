from setuptools import setup, find_packages

setup(
    name="culebra",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'culebra=culebra.interpreter.__main__:main',
            'culebra-repl=culebra.repl:main',
        ],
    },
)