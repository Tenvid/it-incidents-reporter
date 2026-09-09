# it-incidents-reporter

Aplicación web para el registro, consulta y gestión de incidencias IT (equipos,
servidores y servicios de una empresa). Es el proyecto final del Máster
Executive Python Full Stack Developer (INTECSSA): Django es el núcleo del
proyecto, y el análisis de datos con Pandas, el modelo de Machine Learning y
la comprobación de red son funcionalidades complementarias, no sistemas
independientes.

El objetivo no es construir una plataforma compleja, sino demostrar un uso
correcto de Python, Django, Pandas, Machine Learning básico y networking,
con código organizado y fácil de explicar.

## Alcance funcional

- Registro e inicio de sesión de usuarios.
- CRUD de incidencias (crear, consultar, modificar, eliminar).
- Clasificación de incidencias por prioridad (baja / media / alta) y estado
  (abierta / en proceso / cerrada).
- Filtrado por estado y por prioridad.
- Registro del equipo o servicio afectado.
- Dashboard con estadísticas básicas y al menos 3 gráficos (total de
  incidencias, abiertas/cerradas, prioridad alta, por prioridad, por estado,
  evolución temporal).
- Clasificación automática de prioridad mediante un modelo de ML sencillo.
- Comprobación de conectividad de red (ping/socket a un puerto o petición
  HTTP a un equipo/servicio).

## Modelo de datos: Incidencia

| Campo       | Descripción                                    |
| ----------- | ---------------------------------------------- |
| Título      | Nombre de la incidencia                        |
| Descripción | Explicación del problema                       |
| Equipo      | Equipo o servicio afectado                     |
| Fecha       | Fecha de registro                              |
| Prioridad   | Baja, media, alta                              |
| Estado      | Abierta, en proceso, cerrada                   |
| Usuario     | Usuario que registró la incidencia (FK a User) |

## Stack tecnológico

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
| `ipykernel`     | Ejecución de los notebooks (`analisis.ipynb`, `modelo.ipynb`)                                      |
| `pdoc`          | Generación de documentación técnica a partir de los docstrings (equivalente a Doxygen para Python) |

Gestión de entorno y dependencias con [`uv`](https://docs.astral.sh/uv/),
usando `pyproject.toml` (`[project.dependencies]` para runtime,
`[dependency-groups.dev]` para desarrollo) como fuente única de dependencias.
Los comandos de creación de entorno e instalación están recogidos en el
`Makefile` (ver [Comandos habituales](#comandos-habituales)).

Todas las dependencias (runtime y dev) se fijan con versión exacta (`==`),
nunca con rangos (`>=`, `^`, etc.), para garantizar builds reproducibles.

## Estructura de proyecto

```
it-incidents-reporter/
├── manage.py
├── incidents_reporter/        # proyecto Django (settings, urls, wsgi/asgi)
├── incidencias/              # app Django: modelos, vistas, forms, CRUD, dashboard
├── networking/
│   └── comprobacion.py       # comprobación de conectividad (socket/requests)
├── ml/
│   ├── modelo.ipynb           # entrenamiento del modelo de prioridad
│   └── clasificador.py        # carga del modelo entrenado para usarlo desde Django
├── analisis/
│   └── analisis.ipynb         # análisis exploratorio con Pandas
├── tests/                    # tests con pytest
├── informe/                  # informe técnico final (PDF)
└── presentacion/              # presentación final (PPTX)
```

## Convenciones de desarrollo

- Vistas de Django basadas en clases o funciones, manteniendo el CRUD de
  incidencias en la app `incidencias`.
- La lógica de ML (entrenamiento) vive en notebooks; el modelo entrenado se
  serializa (p. ej. `joblib`) y se carga desde Django solo para inferencia,
  sin reentrenar en cada petición.
- La comprobación de red debe poder ejecutarse tanto integrada en la
  aplicación como script independiente (`python networking/comprobacion.py`).
- Evitar sobreingeniería: no añadir DRF, autenticación por tokens, colas de
  tareas ni microservicios — el alcance es una app Django monolítica.
- Todas las funciones y métodos públicos deben documentarse con docstrings
  siguiendo la convención oficial de Python ([PEP 257](https://peps.python.org/pep-0257/)),
  indicando propósito, parámetros y valor de retorno. Esta documentación es
  la fuente de la que `pdoc` genera la documentación técnica del proyecto.

## Comandos habituales

Los comandos habituales del proyecto están centralizados en el `Makefile`
(el entorno se gestiona con `uv`):

```bash
make venv      # Crea el entorno virtual e instala las dependencias con uv
make run       # Ejecuta el servidor de desarrollo (manage.py runserver)
make migrate   # Ejecuta makemigrations y migrate
make qa PATH_ARG=incidencias # Ejecuta ruff check y mypy sobre la ruta indicada
make test      # Ejecuta los tests (carpeta tests/ en la raíz del proyecto)
```
