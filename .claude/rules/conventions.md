# Convenciones de desarrollo

- Vistas de Django basadas en clases (salvo que por algún motivo sea necesario crear una vista basada en funciones.
  Estos motivos pueden ser por simplicidad de código o por limitaciones técnicas),
  manteniendo el CRUD de incidencias en la app `incidents`.
- La lógica de ML (entrenamiento) vive en notebooks (`ml/similarity.ipynb`);
  el modelo entrenado se serializa con `joblib` (`ml/similarity.joblib`) y
  se carga desde Django solo para inferencia, sin reentrenar en cada
  petición. Solo se serializa el vectorizador: las incidencias candidatas se
  vectorizan en cada consulta porque cambian constantemente.
- La comprobación de red debe poder ejecutarse tanto integrada en la
  aplicación como script independiente (`python networking/comprobacion.py`).
- Evitar sobreingeniería: no añadir DRF, autenticación por tokens, colas de
  tareas ni microservicios — el alcance es una app Django monolítica.
  **Única excepción**: el servicio de comprobación de operabilidad
  (`networking/app.py` + `networking/check_api.py`), un microservicio Flask
  aparte consultado directamente desde el navegador. Es deliberado: su
  propósito es comprobar de extremo a extremo que la base de datos, la red
  y un servicio externo funcionan, algo que pierde sentido si Django se
  limita a llamarse a sí mismo. No sienta precedente para futuras
  funcionalidades.
- Todas las funciones y métodos públicos deben documentarse con docstrings
  siguiendo la convención oficial de Python ([PEP 257](https://peps.python.org/pep-0257/)),
  indicando propósito, parámetros y valor de retorno. Esta documentación es
  la fuente de la que `pdoc` genera la documentación técnica del proyecto.
