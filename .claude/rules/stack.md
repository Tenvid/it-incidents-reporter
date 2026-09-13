# Stack tecnológico

- **Backend**: Django (vistas + ORM + auth de sesión, sin API REST).
- **Frontend**: templates de Django con HTML, CSS y JavaScript (sin
  framework JS ni SPA).
- **Admin**: django-jazzmin como tema del panel de administración de Django.
- **Datos**: Pandas para el análisis de incidencias almacenadas.
- **Visualización**: Matplotlib para los gráficos del dashboard y de los
  notebooks de análisis.
- **Machine Learning**: scikit-learn para el modelo de clasificación de
  prioridad.
- **Networking**: `requests` para la comprobación HTTP; `socket` (stdlib)
  para la comprobación de puerto/conectividad.
- **Base de datos**: SQLite (suficiente para el alcance del proyecto).

## Dependencias

### Runtime (producción)

| Paquete          | Uso                                                                  |
| ---------------- | -------------------------------------------------------------------- |
| `django`         | Framework backend, ORM, autenticación, admin                         |
| `django-jazzmin` | Tema del panel de administración de Django                           |
| `pandas`         | Análisis de las incidencias almacenadas                              |
| `scikit-learn`   | Modelo de clasificación automática de prioridad                      |
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
| `ipykernel`     | Ejecución de los notebooks (`analysis.ipynb`, `modelo.ipynb`)                                      |
| `pdoc`          | Generación de documentación técnica a partir de los docstrings (equivalente a Doxygen para Python) |

Gestión de entorno y dependencias con [`uv`](https://docs.astral.sh/uv/),
usando `pyproject.toml` (`[project.dependencies]` para runtime,
`[dependency-groups.dev]` para desarrollo) como fuente única de dependencias.
Los comandos de creación de entorno e instalación están recogidos en
[`commands.md`](commands.md).

Todas las dependencias (runtime y dev) se fijan con versión exacta (`==`),
nunca con rangos (`>=`, `^`, etc.), para garantizar builds reproducibles.
