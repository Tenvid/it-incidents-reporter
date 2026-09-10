.PHONY: venv run migrate qa test test-unit test-integration

PATH_ARG ?= .

# Crea el entorno virtual e instala las dependencias con uv
venv:
	uv venv
	uv sync --all-groups

# Ejecuta el servidor de desarrollo
run:
	uv run python manage.py runserver

# Ejecuta makemigrations y migrate
migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

# Ejecuta ruff check y mypy sobre la ruta indicada (por defecto, todo el proyecto)
# Uso: make qa PATH_ARG=incidencias
qa:
	uv run ruff check $(PATH_ARG)
	uv run mypy $(PATH_ARG)

# Ejecuta los tests (carpeta tests/ en la raíz del proyecto)
test:
	uv run pytest tests

# Ejecuta solo los tests unitarios (tests/unit)
test-unit:
	uv run pytest tests/unit

# Ejecuta solo los tests de integración (tests/integration)
test-integration:
	uv run pytest tests/integration
