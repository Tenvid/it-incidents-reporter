---
name: qa
description: Run this project's quality gate (ruff + mypy + pytest via the Makefile) before considering a change to it-incidents-reporter finished, and interpret failures correctly for this stack.
---

Before saying a change to this repository is done:

1. Run `make qa PATH_ARG=<app-or-path>` (defaults to the whole repo) —
   `ruff check` plus `mypy` with the `django-stubs` plugin.
2. Run `make test` — `pytest tests` at the repo root, not per-app
   `tests.py` files.
3. If `tests/` doesn't exist yet, say so explicitly instead of treating the
   step as passed or silently skipping it.
4. Report failures as `file:line` + message. Don't silence a ruff/mypy rule
   to make a check pass — `RUF012` is already ignored project-wide for
   Django's mutable-class-attribute idiom (see
   `.claude/rules/conventions.md`); no other rule should be suppressed
   without asking first.
5. To run this without filling the main conversation with linter/test
   output, dispatch the `qa-runner` agent instead of running the commands
   inline.
