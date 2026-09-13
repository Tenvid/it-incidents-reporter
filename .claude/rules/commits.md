# Convenciones de commits (Conventional Commits)

Este proyecto sigue [Conventional Commits](https://www.conventionalcommits.org/).
Es la convención que ya sigue el historial real del repositorio (`build(claude):
add claude.md file`, `build: add project dependencies to pyproject`, etc.).

## Formato

```
<tipo>(<scope opcional>): <descripción>

[cuerpo opcional]

[footer opcional]
```

## Reglas

- Mensajes de commit en inglés, en minúsculas, en modo imperativo
  (`add`, no `added` ni `adds`).
- Sin punto final en la línea de asunto.
- Línea de asunto ≤ 72 caracteres.
- Tipos permitidos:
  - `feat`: nueva funcionalidad
  - `fix`: corrección de un bug
  - `docs`: cambios solo en documentación
  - `style`: cambios de formato que no afectan la lógica
  - `refactor`: cambio de código que no corrige un bug ni añade funcionalidad
  - `test`: añadir o corregir tests
  - `build`: dependencias, empaquetado o herramientas de build
    (`pyproject.toml`, `Makefile`, `uv.lock`)
  - `chore`: mantenimiento que no modifica código fuente ni tests
  - `ci`: configuración de integración continua
- Scope recomendado = app/módulo afectado: `incidents`, `user`, `ml`,
  `networking`, `analysis`, `claude` (para configuración de Claude Code).
- Un commit = un cambio lógico; evitar mezclar un refactor con una feature.
- El cuerpo explica el *por qué*, no el *qué* (el diff ya muestra el qué).
- Breaking changes: `!` tras el tipo/scope (p. ej. `feat(incidents)!: ...`)
  o footer `BREAKING CHANGE: <descripción>`.

## Ejemplos

```
feat(incidents): add priority auto-classification via ML model
fix(networking): handle socket timeout when checking service ports
docs(claude): split rules into .claude/rules
build: pin all dependencies to exact versions
```
