# Comandos habituales

Los comandos habituales del proyecto están centralizados en el `Makefile`
(el entorno se gestiona con `uv`):

```bash
make venv      # Crea el entorno virtual e instala las dependencias con uv
make run       # Ejecuta el servidor de desarrollo (manage.py runserver)
make migrate   # Ejecuta makemigrations y migrate
make qa PATH_ARG=incidencias # Ejecuta ruff check y mypy sobre la ruta indicada
make test      # Ejecuta los tests (carpeta tests/ en la raíz del proyecto)
```

`make test` ejecuta `pytest tests`, así que fallará hasta que exista la
carpeta `tests/` en la raíz (ver [`structure.md`](structure.md)).
