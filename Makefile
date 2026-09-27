.PHONY: venv run run-api run-all migrate seed qa test test-unit test-integration

PATH_ARG ?= .

# Crea el entorno virtual e instala las dependencias con uv
venv:
	uv venv
	uv sync --all-groups

# Ejecuta el servidor de desarrollo
run:
	uv run python src/manage.py runserver

# Ejecuta el servicio Flask de comprobación de operabilidad (incidencia aleatoria)
run-api:
	uv run python networking/app.py

# Ejecuta Django y el microservicio Flask a la vez (necesarios juntos para
# incidents:operability); Ctrl+C detiene ambos procesos
run-all:
	$(MAKE) -j2 run run-api

# Ejecuta makemigrations y migrate
migrate:
	uv run python src/manage.py makemigrations
	uv run python src/manage.py migrate

# Rellena la base de datos con incidencias de ejemplo (100 por defecto)
# Uso: make seed ARGS="--count 150 --seed 42"
seed:
	uv run python src/manage.py seed_incidents $(ARGS)

# Ejecuta ruff check y mypy sobre la ruta indicada, relativa a src/ (por defecto, todo el proyecto)
# ml/ y networking/ se incluyen siempre en el ruff check: aunque viven fuera de src/,
# ml/similarity.py y networking/{check_api,app}.py son código real (inferencia y el
# servicio de comprobación de operabilidad), no solo apoyo para notebooks.
# mypy no sigue networking/ automáticamente (a diferencia de ml/, nada en src/ lo
# importa), así que se comprueba con una llamada aparte.
# Uso: make qa PATH_ARG=incidents
qa:
	uv run ruff check src/$(PATH_ARG) ml networking
	uv run mypy src/$(PATH_ARG)
	uv run mypy networking

# Ejecuta los tests (carpeta src/tests/)
test:
	uv run pytest src/tests

# Ejecuta solo los tests unitarios (src/tests/unit)
test-unit:
	uv run pytest src/tests/unit

# Ejecuta solo los tests de integración (src/tests/integration)
test-integration:
	uv run pytest src/tests/integration
