# Weekend flights

## Installing and running
1. Create a virtual environment and activate it
2. Install requirements
3. Install the module with  
    ```
    pip install -e .
    ```
4. Source the private env variables
    ```
    source private.sh
    ```

## Updating (TODO)
- master branch is untouchable without pull request
- before I can merge pull request to master, all tests should be passed
- after I update master, I can pull changes to the prod

## Developer's rules
- every function has to have a docstring
-  every function has to have at least one test
- all the descriprions must be in English, exception is only for text labels

## Logging rules
- there are 3 levels of logs in the project: DEBUG, INFO, ERROR
- root logger configured in set_logger() func in main.py
- every other file inherits logging settings from the `main.py`
- to add logging to a file simply add  
    ```python
    import logging
    LOG = logging.getLogger(__name__)
    ```
- then use it as usual:  
    ```python
    LOG.info("some information to log")
    ```
- logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook

## How to run tests
- activate virtual environment  
    ```bash
    source .venv/bin/activate
    ```
- run tests  
    ```
    make test
    ```

## How to run linters
- flake8 - uses .flake8 configuration file
    ```
    flake8 wf
    ```
- pylint - uses .pylintrc configuration file
    ```
    pylint wf
    ```
- bandit - uses .bandit configuration file
    ```
    bandit -r .
    ```
