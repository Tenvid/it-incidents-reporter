# Comandos habituales

Los comandos habituales del proyecto están centralizados en el `Makefile`
(el entorno se gestiona con `uv`):

```bash
make venv            # Crea el entorno virtual e instala las dependencias con uv
make run              # Ejecuta el servidor de desarrollo (src/manage.py runserver)
make run-api           # Ejecuta el microservicio Flask de comprobación de operabilidad
make run-all           # Ejecuta Django y Flask a la vez (Ctrl+C detiene ambos)
make migrate          # Ejecuta makemigrations y migrate
make seed             # Rellena la BD con incidencias de ejemplo (make seed ARGS="--count 150 --seed 42")
make qa PATH_ARG=incidents # Ejecuta ruff check y mypy sobre src/<ruta indicada>
make test             # Ejecuta todos los tests (src/tests/)
make test-unit        # Ejecuta solo los tests unitarios (src/tests/unit)
make test-integration # Ejecuta solo los tests de integración (src/tests/integration)
```

La comprobación de operabilidad (`incidents:operability`) necesita **dos
procesos a la vez**: `make run` (Django, puerto 8000) y `make run-api`
(Flask, puerto 5001 por defecto); `make run-all` lanza ambos en una sola
terminal (Ctrl+C los detiene a los dos). Copia `.env.example` a `.env` en
la raíz del repo y ajusta `API_HOST`/`API_PORT`/`ALLOWED_ORIGIN`/
`INCIDENT_API_URL` si cambian los puertos o el hostname (p. ej. al
desplegar con Docker).

`src/tests/unit` y `src/tests/integration` son las dos únicas carpetas de
tests del proyecto (ver [`structure.md`](structure.md)); qué va en cada una
se explica en la skill `tests`. Los tests de integración usan una base de
datos SQLite en memoria (ver `DATABASES["default"]["TEST"]` en
`src/incidents_reporter/settings.py`), nunca `db.sqlite3`.

`PATH_ARG` en `make qa` es relativo a `src/` (p. ej. `make qa
PATH_ARG=incidents` comprueba `src/incidents`). `ruff check` incluye siempre
`ml/` y `networking/` además, ya que `ml/similarity.py` y
`networking/{check_api,app}.py` son código real (inferencia y el servicio de
comprobación de operabilidad), no solo apoyo para notebooks. `mypy` sigue
automáticamente `ml/` al seguir el `import` desde `src/incidents`, pero
`networking/` no se importa desde `src/` (es un proceso aparte), así que
`make qa` lo comprueba con una invocación de `mypy` propia.

`make seed` ejecuta el management command `seed_incidents` (opciones
`--count`, `--seed`, `--days`); necesita al menos un usuario existente y no
es idempotente: cada ejecución añade `--count` incidencias nuevas. Sirve
para tener datos en los notebooks (`analysis/`, `dashboard/`, `ml/`) y en la
demo de la app.
