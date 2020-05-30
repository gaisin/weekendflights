"""Setup manifest for Weekend Flights.

NOTE:
    To install or reintall the packages run `pip install -e .`
"""

from setuptools import setup, find_packages

setup(
    name="weekendflights",
    description="Weekend Flights: cheap weekend flights search automated",
    version="0.1",
    author="Rouslan Gaisin",
    author_email="rouslan.gaisin@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "start-wf-parser = wf.app:run_parser_loop",
        ],
    },
)
