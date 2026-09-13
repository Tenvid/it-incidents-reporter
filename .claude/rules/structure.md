# Estructura de proyecto

`src/` contiene únicamente el proyecto Django (settings, apps y tests);
todo lo que no es Django propiamente dicho (`ml/`, `networking/`,
`analisis/`, `informe/`, `presentacion/`) vive en la raíz del repositorio,
deliberadamente separado.

```
it-incidents-reporter/
├── src/
│   ├── manage.py
│   ├── incidents_reporter/    # proyecto Django (settings, urls, wsgi/asgi)
│   ├── user/                  # app Django: usuario propio (auth por email + DNI)
│   ├── incidents/              # app Django: modelos, vistas, forms, CRUD, dashboard
│   ├── static/
│   ├── templates/
│   └── tests/                 # tests con pytest
│       ├── unit/                # tests unitarios (sin BD real o BD trivial)
│       └── integration/         # tests de integración (vistas, flujos CRUD)
├── networking/
│   └── comprobacion.py        # comprobación de conectividad (socket/requests)
├── ml/
│   ├── modelo.ipynb            # entrenamiento del modelo de prioridad
│   └── clasificador.py         # carga del modelo entrenado para usarlo desde Django
├── analisis/
│   └── analisis.ipynb          # análisis exploratorio con Pandas
├── informe/                   # informe técnico final (PDF)
└── presentacion/               # presentación final (PPTX)
```

Nótese que `ml/`, `networking/` y `analisis/` no están (todavía) integrados
en el proyecto Django — no se importan desde `src/`. Son funcionalidades
complementarias que hoy viven fuera de `src/` a propósito; si en el futuro
alguna se invoca desde una vista de `incidents`, habrá que resolver
entonces cómo hacerla importable (p. ej. añadiendo la raíz del repo al
`sys.path` en `settings.py`), no de antemano.

## Estado de implementación

- **Ya implementado**: `src/manage.py`, `src/incidents_reporter/` (proyecto
  Django base), `src/user/` (modelo de usuario propio, registrado como
  `AUTH_USER_MODEL`) e `src/incidents/` (CRUD de incidencias y filtrado por
  estado/prioridad; el dashboard con gráficos queda pendiente dentro de
  esta misma app). `src/tests/unit/` y `src/tests/integration/` existen
  como esqueleto (configurado en `pyproject.toml` y ejecutable vía
  `make test-unit` / `make test-integration` / `make test`), pero están
  vacíos — los ficheros de test de cada app se añaden con la skill `tests`.
- **Pendiente**: `networking/`, `ml/`, `analisis/`, `informe/`,
  `presentacion/` — ninguno existe todavía en el repositorio. El árbol de
  arriba describe la estructura objetivo del proyecto, no el estado actual
  del código. Al crear cada uno, seguir [`conventions.md`](conventions.md).
