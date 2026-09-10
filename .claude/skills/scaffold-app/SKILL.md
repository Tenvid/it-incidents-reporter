---
name: scaffold-app
description: Add one of it-incidents-reporter's still-pending apps/modules (incidencias, ml, networking, analisis) consistent with the project's conventions, when asked to create a new app or module in this repo.
---

it-incidents-reporter is a monolithic Django app. Per
`.claude/rules/structure.md`, only `incidencias`, `ml`, `networking`,
`analisis`, `tests`, `informe` and `presentacion` are still pending. When
asked to create one of them:

1. Place it at the repo root, matching the layout of the existing `user/`
   app (`models.py`, `admin.py`, `managers.py` if needed, `migrations/`).
2. Register new Django apps in `INSTALLED_APPS`
   (`incidents_reporter/settings.py`) — today only `user` is registered.
3. Give every public function/method a PEP 257 docstring (purpose,
   parameters, return value) — `pdoc` builds the project's docs from these.
4. No DRF, token auth, or task queues — function/class-based views and
   session auth only (see `.claude/rules/conventions.md`).
5. ML logic: train in `ml/modelo.ipynb`, serialize with `joblib`, and load
   only for inference in `ml/clasificador.py` — never retrain per request.
6. Networking checks must run both integrated in Django and standalone via
   `python networking/comprobacion.py`.
7. Tests go under the root `tests/` directory (pytest + pytest-django), not
   in a per-app `tests.py`.
8. Finish with the `qa` skill (or the `qa-runner` agent) before calling the
   work done.
