---
name: scaffold-app
description: Add one of it-incidents-reporter's still-pending apps/modules (ml, networking) consistent with the project's conventions, when asked to create a new app or module in this repo.
---

it-incidents-reporter is a monolithic Django app. Per
`.claude/rules/structure.md`, only `ml/similarity.py` (inference module),
`networking`, `informe` and `presentacion` are still pending (`analysis/`,
`dashboard/` and the `ml/` training notebook already exist). When asked to
create one of them:

1. Place it at the repo root — `ml/` and `networking/` are deliberately
   outside `src/`, which holds only the Django project itself (see
   `.claude/rules/structure.md`), same as `analysis/`. They are not (yet)
   imported from a Django app; if that changes later, resolve the import
   path then rather than restructuring in advance.
2. Register new Django apps in `INSTALLED_APPS`
   (`src/incidents_reporter/settings.py`) — today only `user` is
   registered.
3. Give every public function/method a PEP 257 docstring (purpose,
   parameters, return value) — `pdoc` builds the project's docs from these.
4. No DRF, token auth, or task queues — function/class-based views and
   session auth only (see `.claude/rules/conventions.md`).
5. ML logic: train in `ml/similarity.ipynb`, serialize with `joblib` to
   `ml/similarity.joblib`, and load only for inference in
   `ml/similarity.py` — never retrain per request. `build_text` (how title,
   description and equipment are joined) must be identical in training and
   inference: define it in `ml/similarity.py` and import it from the
   notebook.
6. Networking checks must run both integrated in Django and standalone via
   `python networking/comprobacion.py`.
7. Finish with the `qa` skill (or the `qa-runner` agent) before calling the
   work done.
