# Comandos habituales

Los comandos habituales del proyecto están centralizados en el `Makefile`
(el entorno se gestiona con `uv`):

```bash
make venv            # Crea el entorno virtual e instala las dependencias con uv
make run              # Ejecuta el servidor de desarrollo (manage.py runserver)
make migrate          # Ejecuta makemigrations y migrate
make qa PATH_ARG=incidents # Ejecuta ruff check y mypy sobre la ruta indicada
make test             # Ejecuta todos los tests (tests/)
make test-unit        # Ejecuta solo los tests unitarios (tests/unit)
make test-integration # Ejecuta solo los tests de integración (tests/integration)
```

`tests/unit` y `tests/integration` son las dos únicas carpetas de tests del
proyecto (ver [`structure.md`](structure.md)); qué va en cada una se explica
en la skill `tests`. Los tests de integración usan una base de datos SQLite
en memoria (ver `DATABASES["default"]["TEST"]` en
`incidents_reporter/settings.py`), nunca `db.sqlite3`.
