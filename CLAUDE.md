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

## Dónde buscar / qué invocar

| Si necesitas...                                                                | Consulta / invoca                                              |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Alcance funcional y modelo de datos                                            | [`.claude/rules/domain.md`](.claude/rules/domain.md)           |
| Stack tecnológico y dependencias                                               | [`.claude/rules/stack.md`](.claude/rules/stack.md)             |
| Estructura de carpetas del proyecto                                            | [`.claude/rules/structure.md`](.claude/rules/structure.md)     |
| Convenciones de desarrollo (vistas, ML, networking, docstrings)                | [`.claude/rules/conventions.md`](.claude/rules/conventions.md) |
| Comandos habituales (`make ...`)                                               | [`.claude/rules/commands.md`](.claude/rules/commands.md)       |
| Formato de los mensajes de commit                                              | [`.claude/rules/commits.md`](.claude/rules/commits.md)         |
| Dar por terminado un cambio de código (lint, tipos, tests)                     | skill `qa` (o agente `qa-runner`)                              |
| Crear una app/módulo pendiente (`ml`, `networking`, `analisis`)                | skill `scaffold-app`                                           |
| Auditar docstrings PEP 257 antes de generar docs con `pdoc`                    | agente `docstring-check`                                       |
