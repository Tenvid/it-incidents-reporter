# Convenciones de desarrollo

- Vistas de Django basadas en clases (salvo que por algún motivo sea necesario crear una vista basada en funciones.
  Estos motivos pueden ser por simplicidad de código o por limitaciones técnicas),
  manteniendo el CRUD de incidencias en la app `incidents`.
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
