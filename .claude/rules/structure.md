# Estructura de proyecto

`src/` contiene únicamente el proyecto Django (settings, apps y tests);
todo lo que no es Django propiamente dicho (`ml/`, `networking/`,
`analysis/`, `dashboard/`, `informe/`, `presentacion/`) vive en la raíz
del repositorio, deliberadamente separado.

```
it-incidents-reporter/
├── src/
│   ├── manage.py
│   ├── incidents_reporter/    # proyecto Django (settings, urls, wsgi/asgi)
│   ├── user/                  # app Django: usuario propio (auth por email + DNI)
│   ├── incidents/              # app Django: modelos, vistas, forms, CRUD, dashboard
│   │   └── management/commands/seed_incidents.py  # datos de ejemplo (make seed)
│   ├── static/
│   ├── templates/
│   └── tests/                 # tests con pytest
│       ├── unit/                # tests unitarios (sin BD real o BD trivial)
│       └── integration/         # tests de integración (vistas, flujos CRUD)
├── networking/
│   ├── comprobacion.py        # comprobación de conectividad (socket/requests) — pendiente
│   ├── check_api.py           # lee y formatea una incidencia aleatoria (sin Django)
│   └── app.py                 # servicio Flask que expone check_api.py vía HTTP (make run-api)
├── ml/
│   ├── similarity.ipynb        # entrenamiento del modelo de similitud (TF-IDF)
│   ├── similarity.joblib       # vectorizador entrenado, generado por el notebook
│   └── similarity.py           # carga del vectorizador e inferencia, usado desde incidents
├── analysis/
│   └── analysis.ipynb          # análisis exploratorio con Pandas
├── dashboard/
│   └── dashboard.ipynb         # dashboard de estadísticas y gráficos con Pandas/Matplotlib
├── informe/                   # informe técnico final (PDF)
└── presentacion/               # presentación final (PPTX)
```

`analysis/` y `dashboard/` no están (todavía) integrados en el proyecto
Django — no se importan desde `src/`. Son funcionalidades complementarias
que hoy viven fuera de `src/` a propósito; si en el futuro alguna se invoca
desde una vista de `incidents`, se resolverá su importabilidad entonces (no
de antemano), siguiendo el mismo patrón ya aplicado a `ml/`.

`networking/` mezcla dos cosas con estados distintos: `comprobacion.py`
sigue pendiente y, cuando se integre, seguirá el mismo patrón de import que
`ml/`. `check_api.py` y `app.py` ya están integrados, pero no por import:
son el microservicio Flask aparte que documenta la excepción en
[`conventions.md`](conventions.md), y la página `incidents:operability` lo
consulta por HTTP desde el navegador, nunca desde Python.

`ml/` es la primera excepción: `ml/similarity.py` sí se importa desde
`src/incidents/views.py` (para sugerir incidencias similares al crear una),
gracias a que `src/incidents_reporter/settings.py` añade la raíz del repo a
`sys.path`. La dependencia va en un solo sentido — Django importa `ml/`,
nunca al revés — así que `ml/` sigue sin importar Django ni su ORM.

`analysis/`, `dashboard/` y `ml/` ya existen (`analysis.ipynb`,
`dashboard.ipynb` y `similarity.ipynb`, código y nombres en inglés); los
tres notebooks leen `src/db.sqlite3` en solo lectura, sin Django, y se
ejecutan desde la raíz del repositorio. `ml/similarity.py` y `networking/`
siguen pendientes.

## Estado de implementación

- **Ya implementado**: `src/manage.py`, `src/incidents_reporter/` (proyecto
  Django base), `src/user/` (modelo de usuario propio, registrado como
  `AUTH_USER_MODEL`) e `src/incidents/` (CRUD de incidencias, filtrado por
  estado/prioridad, y la comprobación de operabilidad en
  `incidents:operability`; el dashboard con gráficos queda pendiente dentro
  de esta misma app). `src/tests/unit/` y `src/tests/integration/` están
  configuradas en `pyproject.toml` y son ejecutables vía `make test-unit` /
  `make test-integration` / `make test`; ya tienen tests para `incidents`
  (CRUD, duplicados, comprobación de operabilidad) y el comando `seed` — los
  ficheros de test de cada app nueva se añaden con la skill `tests`.
  También está implementado el análisis de datos en `analysis/analysis.ipynb`
  y el dashboard en `dashboard/dashboard.ipynb`, ambos fuera de `src/`. El
  dashboard del notebook es un artefacto aparte: el dashboard con gráficos
  dentro de la app `incidents` (vista Django) sigue pendiente por separado.
  El management command `seed_incidents` (`make seed`) genera incidencias de
  ejemplo para los notebooks y la demo. Del módulo `ml/` existe el notebook
  de entrenamiento `similarity.ipynb`, el vectorizador serializado
  `similarity.joblib` y `similarity.py` (inferencia), ya integrado en
  `incidents`: un botón "Check dupes" en el formulario de creación envía el
  título/descripción/equipo por AJAX a una vista que puntúa la incidencia
  contra las abiertas/en proceso y muestra las coincidencias en un modal.
  Del módulo `networking/`, `check_api.py` y `app.py` están implementados
  (ver más arriba); `comprobacion.py` sigue pendiente.
- **Pendiente**: la sugerencia de incidencias similares en la vista de
  detalle (la otra mitad de lo descrito en [`domain.md`](domain.md)),
  `networking/comprobacion.py`, `informe/`, `presentacion/`, y el dashboard
  integrado en la app `incidents`. El árbol de arriba describe la
  estructura objetivo del proyecto, no el estado actual del código. Al
  crear cada uno, seguir [`conventions.md`](conventions.md).
