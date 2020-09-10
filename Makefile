test:
	source private.sh && pytest -vvvv --cov=./wf

lint:
	flake8 wf