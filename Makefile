all: run

run:
	PYTHONPATH=. python backseat_driver/backseat_driver.py

install:
	pip install -r requirements.txt

lint:
	pylint backseat_driver
	pylint tests

test:
	pytest --cov=backseat_driver tests

format:
	black .
