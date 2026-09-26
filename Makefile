.PHONY: venv run migrate seed qa test test-unit test-integration

PATH_ARG ?= .

# Crea el entorno virtual e instala las dependencias con uv
venv:
	uv venv
	uv sync --all-groups

# Ejecuta el servidor de desarrollo
run:
	uv run python src/manage.py runserver

# Ejecuta makemigrations y migrate
migrate:
	uv run python src/manage.py makemigrations
	uv run python src/manage.py migrate

# Rellena la base de datos con incidencias de ejemplo (100 por defecto)
# Uso: make seed ARGS="--count 150 --seed 42"
seed:
	uv run python src/manage.py seed_incidents $(ARGS)

# Ejecuta ruff check y mypy sobre la ruta indicada, relativa a src/ (por defecto, todo el proyecto)
# ml/ se incluye siempre en el ruff check: aunque vive fuera de src/, ml/similarity.py
# es código de inferencia que importa la app incidents, no solo un notebook de apoyo.
# Uso: make qa PATH_ARG=incidents
qa:
	uv run ruff check src/$(PATH_ARG) ml
	uv run mypy src/$(PATH_ARG)

# Ejecuta los tests (carpeta src/tests/)
test:
	uv run pytest src/tests

# Ejecuta solo los tests unitarios (src/tests/unit)
test-unit:
	uv run pytest src/tests/unit

# Ejecuta solo los tests de integración (src/tests/integration)
test-integration:
	uv run pytest src/tests/integration
