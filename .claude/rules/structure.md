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
│   └── comprobacion.py        # comprobación de conectividad (socket/requests)
├── ml/
│   ├── similarity.ipynb        # entrenamiento del modelo de similitud (TF-IDF)
│   ├── similarity.joblib       # vectorizador entrenado, generado por el notebook
│   └── similarity.py           # (pendiente) carga del modelo para inferencia desde Django
├── analysis/
│   └── analysis.ipynb          # análisis exploratorio con Pandas
├── dashboard/
│   └── dashboard.ipynb         # dashboard de estadísticas y gráficos con Pandas/Matplotlib
├── informe/                   # informe técnico final (PDF)
└── presentacion/               # presentación final (PPTX)
```

Nótese que `ml/`, `networking/`, `analysis/` y `dashboard/` no están
(todavía) integrados en el proyecto Django — no se importan desde `src/`.
Son funcionalidades complementarias que hoy viven fuera de `src/` a
propósito; si en el futuro alguna se invoca desde una vista de
`incidents`, habrá que resolver entonces cómo hacerla importable (p. ej.
añadiendo la raíz del repo al `sys.path` en `settings.py`), no de
antemano.

`analysis/`, `dashboard/` y `ml/` ya existen (`analysis.ipynb`,
`dashboard.ipynb` y `similarity.ipynb`, código y nombres en inglés); los
tres notebooks leen `src/db.sqlite3` en solo lectura, sin Django, y se
ejecutan desde la raíz del repositorio. `ml/similarity.py` y `networking/`
siguen pendientes.

## Estado de implementación

- **Ya implementado**: `src/manage.py`, `src/incidents_reporter/` (proyecto
  Django base), `src/user/` (modelo de usuario propio, registrado como
  `AUTH_USER_MODEL`) e `src/incidents/` (CRUD de incidencias y filtrado por
  estado/prioridad; el dashboard con gráficos queda pendiente dentro de
  esta misma app). `src/tests/unit/` y `src/tests/integration/` existen
  como esqueleto (configurado en `pyproject.toml` y ejecutable vía
  `make test-unit` / `make test-integration` / `make test`), pero están
  vacíos — los ficheros de test de cada app se añaden con la skill `tests`.
  También está implementado el análisis de datos en `analysis/analysis.ipynb`
  y el dashboard en `dashboard/dashboard.ipynb`, ambos fuera de `src/`. El
  dashboard del notebook es un artefacto aparte: el dashboard con gráficos
  dentro de la app `incidents` (vista Django) sigue pendiente por separado.
  El management command `seed_incidents` (`make seed`) genera incidencias de
  ejemplo para los notebooks y la demo. Del módulo `ml/` existe el notebook
  de entrenamiento `similarity.ipynb` y el vectorizador serializado
  `similarity.joblib`.
- **Pendiente**: `ml/similarity.py` (inferencia) y su integración en la app
  `incidents` (sugerir incidencias similares al crear y en el detalle),
  `networking/`, `informe/`, `presentacion/`, y el dashboard integrado en la
  app `incidents`. El árbol de arriba describe la estructura objetivo del
  proyecto, no el estado actual del código. Al crear cada uno, seguir
  [`conventions.md`](conventions.md).
