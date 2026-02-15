setup:
	uv venv --python 3.14
	uv sync --group dev

checkformat:
	.venv/bin/ruff check
	
test:
	.venv/bin/pytest -m unit

