# Estructura de proyecto

```
it-incidents-reporter/
├── manage.py
├── incidents_reporter/        # proyecto Django (settings, urls, wsgi/asgi)
├── user/                      # app Django: usuario propio (auth por email + DNI)
├── incidents/                  # app Django: modelos, vistas, forms, CRUD, dashboard
├── networking/
│   └── comprobacion.py        # comprobación de conectividad (socket/requests)
├── ml/
│   ├── modelo.ipynb            # entrenamiento del modelo de prioridad
│   └── clasificador.py         # carga del modelo entrenado para usarlo desde Django
├── analisis/
│   └── analisis.ipynb          # análisis exploratorio con Pandas
├── tests/                     # tests con pytest
│   ├── unit/                   # tests unitarios (sin BD real o BD trivial)
│   └── integration/            # tests de integración (vistas, flujos CRUD)
├── informe/                   # informe técnico final (PDF)
└── presentacion/               # presentación final (PPTX)
```

## Estado de implementación

- **Ya implementado**: `manage.py`, `incidents_reporter/` (proyecto Django
  base), `user/` (modelo de usuario propio, registrado como
  `AUTH_USER_MODEL`) e `incidents/` (CRUD de incidencias y filtrado por
  estado/prioridad; el dashboard con gráficos queda pendiente dentro de
  esta misma app). `tests/unit/` y `tests/integration/` existen como
  esqueleto (configurado en `pyproject.toml` y ejecutable vía
  `make test-unit` / `make test-integration` / `make test`), pero están
  vacíos — los ficheros de test de cada app se añaden con la skill `tests`.
- **Pendiente**: `networking/`, `ml/`, `analisis/`, `informe/`,
  `presentacion/` — ninguno existe todavía en el repositorio. El árbol de
  arriba describe la estructura objetivo del proyecto, no el estado actual
  del código. Al crear cada uno, seguir [`conventions.md`](conventions.md).
