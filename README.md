# Weekend flights

## Installing and running
1. Install git, docker and docker-compose
2. Clone repo
    ```sh
    git clone https://github.com/gaisin/weekendflights.git
    ```
3. Add `private.env` file with environment variables to project's root folder
4. Run containers with docker-compose
    ```sh
    docker-compose up -d
    ```
You are brilliant!

## Debugging
- To test changes inside of container use next command to force docker rebuild image
    ```sh
    docker-compose up --build --force-recreate -d
    ```
- To enter docker container use
    ```sh
    docker exec -it <container-id> bash
    ```
- To see logs use
    ```sh
    docker logs <container-id> -f
    ```

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
