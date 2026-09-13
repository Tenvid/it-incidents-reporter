---
name: tests
description: Write pytest unit and integration tests for an app in it-incidents-reporter — pure logic (models, forms, validators, managers) as unit tests under src/tests/unit/, DB/view-backed flows as integration tests under src/tests/integration/ — runnable via `make test-unit`, `make test-integration`, or `make test`. Use when asked to add or write tests for an app.
---

When asked to add or write tests for an app in this repo:

1. **Placement**: pure logic with no or trivial DB access (validators,
   model `__str__`/`get_absolute_url`, manager methods, form `clean`
   methods) goes in `src/tests/unit/`; anything exercising views, URL
   routing, the Django test client, or a multi-component CRUD flow goes in
   `src/tests/integration/`. Name files
   `src/tests/unit/test_<app>_<subject>.py` /
   `src/tests/integration/test_<app>_<subject>.py` (e.g.
   `src/tests/unit/test_user_validators.py`,
   `src/tests/integration/test_incident_views.py`).
2. **Style**: plain pytest functions, not `unittest.TestCase`. Mark
   DB-touching tests with `@pytest.mark.django_db` or use a fixture that
   implies DB access (`client`, `django_user_model`). Reuse an existing
   `src/tests/conftest.py` fixture instead of duplicating setup across
   files; add one only once two or more files need the same fixture.
   `DATABASES["default"]["TEST"]["NAME"]` is `:memory:` (see
   `src/incidents_reporter/settings.py`), so `django_db`-marked tests never
   touch `db.sqlite3` — never point a test at the dev database directly.
3. **Views**: use Django's test `Client`. Cover the `LoginRequiredMixin`
   redirect-when-anonymous case, the CRUD happy path, and any custom
   `get_queryset` filtering (e.g. `src/incidents/views.py`
   `IncidentListView`).
4. **Docstrings**: test functions don't need PEP 257 docstrings — `pdoc`
   doesn't document `src/tests/` (see `.claude/rules/structure.md`). Use
   descriptive names instead (`test_<what>_<condition>_<expected>`).
5. Run `make test-unit`, `make test-integration`, or `make test` (all) to
   verify — the environment is managed by `uv` (see `Makefile`).
6. Finish with the `qa` skill (ruff + mypy + pytest) before considering the
   tests done.
