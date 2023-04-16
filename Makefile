all: run

run:
	PYTHONPATH=. python backseat_driver/backseat_driver.py $(shell find . -name "*.py")

install:
	pip install -r requirements.txt

lint:
	pylint backseat_driver
	pylint tests

test:
	pytest --cov=backseat_driver tests

format:
	black .

package:
	rm -rf dist
	python3 -m build
	python3 -m twine upload dist/*
