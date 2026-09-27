# IT Incidents Reporter

> 🇬🇧 English version: [README-eng.md](README-eng.md)

![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-6.1-092E20?logo=django&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

Aplicación web para el registro, consulta y gestión de incidencias IT
(equipos, servidores y servicios) de una empresa, con detección de
posibles duplicados mediante Machine Learning y una comprobación de
operabilidad extremo a extremo del sistema.

Es el proyecto final del Máster Executive Python Full Stack Developer (INTECSSA):
Django es el núcleo de la aplicación, y el análisis de datos con Pandas,
el modelo de Machine Learning y la comprobación de red son funcionalidades
complementarias, no sistemas independientes.

## Qué problema resuelve

Cuando una empresa gestiona incidencias de IT a mano (hojas de cálculo,
tickets sueltos, correos), es fácil perder de vista qué está abierto, qué
es urgente, y detectar que dos personas han reportado el mismo problema
con palabras distintas. Esta aplicación centraliza el registro y
seguimiento de incidencias, las clasifica por prioridad y estado, permite
filtrarlas, ofrece un dashboard con estadísticas para quien administra el
sistema, sugiere posibles duplicados al crear una incidencia nueva, y
permite comprobar de un vistazo que la base de datos, la red y un
servicio externo del sistema siguen operativos.

## Funcionalidades

- **Autenticación propia**: registro e inicio de sesión con un modelo de
  usuario propio que autentica por email en lugar de username, con DNI
  español validado (formato + letra de control).
- **CRUD de incidencias**: crear, consultar, modificar y eliminar
  incidencias (título, descripción, equipo/servicio afectado, fecha,
  prioridad, estado, usuario).
- **Clasificación y filtrado**: prioridad (baja / media / alta) y estado
  (abierta / en proceso / cerrada), con filtrado por ambos campos.
- **Dashboard administrativo**: solo para administradores, con 4 KPIs y 4
  gráficos interactivos (por prioridad, por estado, por equipo, y
  evolución temporal con selector de granularidad día/semana/mes/año),
  calculados con el ORM de Django.
- **Detección de duplicados (ML)**: al crear una incidencia, un botón
  "Check dupes" la compara mediante TF-IDF y similitud coseno contra las
  incidencias abiertas/en proceso, y muestra las coincidencias en un
  modal.
- **Comprobación de operabilidad extremo a extremo**: un botón pide,
  mediante una petición HTTP directa desde el navegador, una incidencia
  aleatoria no archivada al microservicio Flask, confirmando que la base
  de datos, la red y ese servicio externo funcionan juntos.

## Stack tecnológico

| Categoría                       | Tecnología                               | Uso                                                                   |
| ------------------------------- | ---------------------------------------- | --------------------------------------------------------------------- |
| Backend                         | Django 6.1                               | Vistas basadas en clases, ORM, autenticación de sesión (sin API REST) |
| Admin                           | django-jazzmin                           | Tema del panel de administración de Django                            |
| Frontend                        | Templates de Django + HTML/CSS/JS        | Sin framework JS ni SPA                                               |
| Visualización (dashboard admin) | ApexCharts (vendorizado, sin CDN)        | Gráficos interactivos de `incidents:dashboard`                        |
| Data analysis                   | Pandas                                   | Análisis de las incidencias almacenadas                               |
| Visualización (notebooks)       | Matplotlib                               | Gráficos de `analysis/` y `dashboard/`                                |
| Machine Learning                | scikit-learn (TF-IDF + similitud coseno) | Detección de incidencias duplicadas                                   |
| Serialización del modelo        | joblib                                   | Vectorizador TF-IDF entrenado (`ml/similarity.joblib`)                |
| Networking                      | requests                                 | Comprobación de conectividad HTTP / puerto                            |
| Microservicio de operabilidad   | Flask                                    | Endpoint que expone una incidencia aleatoria vía JSON                 |
| Base de datos                   | SQLite (con posibilidad de migración)    | Persistencia                                                          |
| Entorno y dependencias          | uv                                       | Entorno virtual y dependencias fijadas con versión exacta             |
| Calidad de código               | ruff, mypy, django-stubs                 | Linting, formateo y comprobación estática de tipos                    |
| Tests                           | pytest, pytest-django                    | Tests unitarios y de integración                                      |
| Documentación técnica           | pdoc                                     | Documentación generada a partir de docstrings PEP 257                 |

## Estructura del proyecto

```
it-incidents-reporter/
├── src/                        # Proyecto Django
│   ├── manage.py
│   ├── incidents_reporter/     # Configuración del proyecto (settings, urls, wsgi/asgi)
│   ├── user/                   # App: usuario propio (auth por email + DNI)
│   ├── incidents/              # App: CRUD de incidencias, dashboard, operabilidad
│   ├── static/                 # CSS y JS (incluye ApexCharts vendorizado)
│   ├── templates/               # Plantillas base
│   └── tests/                  # Tests con pytest (unit/ e integration/)
├── ml/                         # Detección de incidencias similares
│   ├── similarity.ipynb        # Entrenamiento del modelo (TF-IDF)
│   ├── similarity.joblib       # Vectorizador entrenado, generado por el notebook
│   └── similarity.py           # Inferencia, importado desde src/incidents
├── networking/                 # Comprobación de operabilidad extremo a extremo
│   ├── app.py                  # Microservicio Flask (make run-api)
│   └── check_api.py            # Lectura de una incidencia aleatoria (sqlite3, sin ORM)
├── analysis/
│   └── analysis.ipynb          # Análisis exploratorio con Pandas
├── dashboard/
│   └── dashboard.ipynb         # Dashboard complementario con Matplotlib
├── Makefile
├── pyproject.toml
├── .env.example
└── LICENSE
```

`ml/`, `networking/`, `analysis/` y `dashboard/` viven deliberadamente
fuera de `src/`: solo `ml/similarity.py` se importa desde Django (para la
inferencia de similitud); el resto son notebooks de análisis o el
microservicio Flask, que se consulta por HTTP directamente desde el
navegador, nunca desde Python.

## Requisitos

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Instalación

```bash
git clone https://github.com/Tenvid/it-incidents-reporter.git
cd it-incidents-reporter

make venv                            # crea el entorno virtual e instala dependencias con uv
cp .env.example .env                 # ajusta host/puerto si hace falta

make migrate                         # aplica las migraciones
uv run python src/manage.py createsuperuser   # necesario para el dashboard admin

make seed                            # opcional: incidencias de ejemplo (ARGS="--count 150 --seed 42")
```

## Ejecución

La comprobación de operabilidad (`incidents:operability`) necesita **dos
procesos a la vez**: Django y el microservicio Flask. Se pueden ejecutar por separado:

```bash
make run       # Django, http://localhost:8000
make run-api   # Flask, http://localhost:5001 (por defecto)

```

O a la vez

```bash
make run-all   # ambos a la vez, en una sola terminal (Ctrl+C detiene los dos)
```

## Tests y calidad de código

```bash
make test               # todos los tests (src/tests/)
make test-unit          # solo tests unitarios (src/tests/unit)
make test-integration   # solo tests de integración (src/tests/integration)

make qa PATH_ARG=incidents   # ruff check + mypy sobre src/incidents (+ ml/ y networking/ siempre)
```

Los tests de integración usan una base de datos SQLite en memoria, nunca
`db.sqlite3`.

## Documentación técnica

La documentación se genera con `pdoc` a partir de los docstrings (PEP 257)
de `src/incidents`, `src/user` e `src/incidents_reporter`:

```bash
cd src
DJANGO_SETTINGS_MODULE=incidents_reporter.settings uv run python -c "
import django; django.setup()
import pdoc
from pathlib import Path
pdoc.pdoc('incidents', 'user', 'incidents_reporter', output_directory=Path('../docs'))
"
```

## Modelo de Machine Learning

El entrenamiento del vectorizador TF-IDF vive en un notebook
(`ml/similarity.ipynb`); solo se serializa el vectorizador
(`ml/similarity.joblib`) con `joblib`, ya que las incidencias candidatas
cambian constantemente y se vectorizan en cada consulta. `ml/similarity.py`
carga el vectorizador y realiza la inferencia desde Django, sin
reentrenar en cada petición.

## Notebooks complementarios

`analysis/analysis.ipynb` (análisis exploratorio con Pandas) y
`dashboard/dashboard.ipynb` (gráficos con Matplotlib) son funcionalidades
complementarias que no se importan desde Django: leen `src/db.sqlite3` en
solo lectura y se ejecutan desde la raíz del repositorio. El dashboard del
notebook es un artefacto aparte, independiente del dashboard integrado en
`incidents:dashboard`.

## Licencia

Distribuido bajo licencia [MIT](LICENSE).

## Autor

**David Gómez Barberá**

- LinkedIn: [david-gomez-barbera](https://www.linkedin.com/in/david-gomez-barbera/)
- Email: [davidgb.business@gmail.com](mailto:davidgb.business@gmail.com)
