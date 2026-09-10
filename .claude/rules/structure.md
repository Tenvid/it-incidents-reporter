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
├── informe/                   # informe técnico final (PDF)
└── presentacion/               # presentación final (PPTX)
```

## Estado de implementación

- **Ya implementado**: `manage.py`, `incidents_reporter/` (proyecto Django
  base) y `user/` (modelo de usuario propio, registrado como
  `AUTH_USER_MODEL`).
- **Pendiente**: `incidencias/`, `networking/`, `ml/`, `analisis/`,
  `tests/`, `informe/`, `presentacion/` — ninguno existe todavía en el
  repositorio. El árbol de arriba describe la estructura objetivo del
  proyecto, no el estado actual del código. Al crear cada uno, seguir
  [`conventions.md`](conventions.md).
