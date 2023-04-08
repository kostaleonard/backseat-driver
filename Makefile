all: run

run:
	PYTHONPATH=. python backseat_driver/backseat_driver.py --filter_files_by_suffix ".py"

install:
	pip install -r requirements.txt

lint:
	pylint backseat_driver
	pylint tests

test:
	pytest --cov=backseat_driver tests

format:
	black .
