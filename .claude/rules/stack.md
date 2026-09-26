# Stack tecnológico

- **Backend**: Django (vistas + ORM + auth de sesión, sin API REST).
- **Frontend**: templates de Django con HTML, CSS y JavaScript (sin
  framework JS ni SPA).
- **Admin**: django-jazzmin como tema del panel de administración de Django.
- **Datos**: Pandas para el análisis de incidencias almacenadas.
- **Visualización**: Matplotlib para los gráficos del dashboard y de los
  notebooks de análisis.
- **Machine Learning**: scikit-learn para el modelo de similitud de
  incidencias (`TfidfVectorizer` + similitud coseno), serializado con
  `joblib` (dependencia transitiva de scikit-learn).
- **Networking**: `requests` para la comprobación HTTP; `socket` (stdlib)
  para la comprobación de puerto/conectividad.
- **Comprobación de operabilidad**: Flask sirve un único endpoint
  (`networking/app.py`, puerto configurable) que lee una incidencia
  aleatoria de `db.sqlite3` con `sqlite3` (stdlib, sin ORM) y la devuelve
  como JSON; la página Django la consulta con `fetch()` directamente desde
  el navegador (no vía Django), por lo que el servicio añade su propia
  cabecera CORS a mano (`after_request`, sin `flask-cors`) en vez de un
  proxy Django. Es la única excepción documentada al alcance monolítico
  (ver [`conventions.md`](conventions.md)).
- **Base de datos**: SQLite (suficiente para el alcance del proyecto).

## Dependencias

### Runtime (producción)

| Paquete          | Uso                                                                  |
| ---------------- | -------------------------------------------------------------------- |
| `django`         | Framework backend, ORM, autenticación, admin                         |
| `django-jazzmin` | Tema del panel de administración de Django                           |
| `flask`          | Microservicio de comprobación de operabilidad (`networking/app.py`)  |
| `pandas`         | Análisis de las incidencias almacenadas                              |
| `scikit-learn`   | Modelo de similitud para detectar incidencias duplicadas             |
| `matplotlib`     | Gráficos del dashboard (total, por prioridad, por estado, evolución) |
| `requests`       | Comprobación HTTP de un equipo/servicio                              |
| `python-dotenv`  | Carga de variables de entorno (`SECRET_KEY`, `DEBUG`, etc.)          |

### Desarrollo

| Paquete         | Uso                                                                                                |
| --------------- | -------------------------------------------------------------------------------------------------- |
| `ruff`          | Linting y formateo                                                                                 |
| `mypy`          | Comprobación estática de tipos                                                                     |
| `django-stubs`  | Tipos de Django para mypy                                                                          |
| `pytest`        | Framework de testing                                                                               |
| `pytest-django` | Integración de pytest con Django                                                                   |
| `ipykernel`     | Ejecución de los notebooks (`analysis.ipynb`, `dashboard.ipynb`, `similarity.ipynb`)               |
| `pdoc`          | Generación de documentación técnica a partir de los docstrings (equivalente a Doxygen para Python) |

Gestión de entorno y dependencias con [`uv`](https://docs.astral.sh/uv/),
usando `pyproject.toml` (`[project.dependencies]` para runtime,
`[dependency-groups.dev]` para desarrollo) como fuente única de dependencias.
Los comandos de creación de entorno e instalación están recogidos en
[`commands.md`](commands.md).

Todas las dependencias (runtime y dev) se fijan con versión exacta (`==`),
nunca con rangos (`>=`, `^`, etc.), para garantizar builds reproducibles.
