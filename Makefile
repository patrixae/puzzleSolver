.PHONY: check format typing linting check-format test eval prepare prepare-dev

check: format typing linting

format:
	@black --line-length=100 puzzle_solver

typing:
	@mypy puzzle_solver

linting:
	@pylint puzzle_solver

check-format:
	@black --line-length=100 --check --diff puzzle_solver

test:
	@python -m pytest test

eval:
	@python -m pytest eval

benchmark:
	@python -m pytest benchmarking

prepare:
	@pip install -e .

prepare-dev:
	@pip install -e '.[dev]'
