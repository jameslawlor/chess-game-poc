.PHONY: all
# Clean temporary and generated files
all: ruff tests clean

.PHONY: clean
# Clean temporary and generated files
clean:
	find . \( -type f -name '*.pyc' -or -type d -name '__pycache__*' \) -delete
	find . \( -type d -name '.eggs' -or -type d -name '*.egg-info' -or -type d -name '.pytest_cache' \) | xargs rm -rf
	ruff clean
	
.PHONY: lint format check ruff
ruff:
	ruff format .
	ruff check .
	
lint:
	ruff check . --exit-zero

format:
	ruff format .

check: lint

.PHONY: tests
tests:
	pytest -vs