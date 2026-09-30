# IT Incidents Reporter

> 🇪🇸 Versión en español: [README.md](README.md)

![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-6.1-092E20?logo=django&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

Web application for registering, browsing and managing a company's IT
incidents (equipment, servers and services), with duplicate-incident
detection via Machine Learning and an end-to-end operability check of the
system.

It's the final project of the Executive Python Full Stack Developer
Master's degree (INTECSSA): Django is the core of the application, while
data analysis with Pandas, the Machine Learning model and the network
check are complementary features, not standalone systems.

## What problem it solves

When a company tracks IT incidents by hand (spreadsheets, loose tickets,
emails), it's easy to lose track of what's open, what's urgent, and to
miss that two people reported the same problem in different words. This
application centralizes incident tracking, classifies incidents by
priority and status, lets you filter them, offers a dashboard with
statistics for administrators, suggests possible duplicates when creating
a new incident, and lets you check at a glance that the database, the
network and an external service of the system are still operational.

## Features

- **Custom authentication**: sign-up and login with a custom user model
  that authenticates by email instead of username, with a validated
  Spanish national ID (format + control letter) as a required field.
- **Incident CRUD**: create, view, update and delete incidents (title,
  description, affected team/service, date, priority, status, user).
- **Classification and filtering**: priority (low / medium / high) and
  status (open / in progress / closed), filterable by both fields.
- **Admin dashboard**: admin-only, with 4 KPIs and 4 interactive charts
  (by priority, by status, by team, and a time-series evolution chart
  with a day/week/month/year granularity selector), computed with
  Django's ORM.
- **Duplicate detection (ML)**: when creating an incident, a "Check
  dupes" button scores it via TF-IDF and cosine similarity against
  open/in-progress incidents and shows the matches in a modal.
- **End-to-end operability check**: a button requests, via a direct HTTP
  call from the browser, a random non-archived incident from the Flask
  microservice, confirming that the database, the network and that
  external service all work together.

## Tech stack

| Category                        | Technology                              | Purpose                                                              |
| --------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| Backend                           | Django 6.1                               | Class-based views, ORM, session authentication (no REST API)          |
| Admin                              | django-jazzmin                           | Django admin panel theme                                              |
| Frontend                          | Django templates + HTML/CSS/JS            | No JS framework, no SPA                                                |
| Visualization (admin dashboard)    | ApexCharts (vendored, no CDN)              | Interactive charts for `incidents:dashboard`                          |
| Data analysis                      | Pandas                                   | Analysis of stored incidents                                          |
| Visualization (notebooks)          | Matplotlib                                | Charts in `analysis/` and `dashboard/`                                 |
| Machine Learning                  | scikit-learn (TF-IDF + cosine similarity) | Duplicate incident detection                                          |
| Model serialization                | joblib                                    | Trained TF-IDF vectorizer (`ml/similarity.joblib`)                     |
| Networking                        | requests                                  | HTTP / port connectivity check                                        |
| Operability microservice           | Flask                                     | Endpoint that exposes a random incident as JSON                       |
| Database                          | SQLite (with room to migrate)             | Persistence                                                            |
| Environment and dependencies       | uv                                        | Virtual environment and exact-pinned dependencies                     |
| Code quality                       | ruff, mypy, django-stubs                    | Linting, formatting and static type checking                          |
| Tests                              | pytest, pytest-django                       | Unit and integration tests                                             |
| Technical documentation             | pdoc                                       | Documentation generated from PEP 257 docstrings                        |

## Project structure

```
it-incidents-reporter/
├── src/                        # Django project
│   ├── manage.py
│   ├── incidents_reporter/     # Project configuration (settings, urls, wsgi/asgi)
│   ├── user/                   # App: custom user (email + national ID auth)
│   ├── incidents/              # App: incident CRUD, dashboard, operability check
│   ├── static/                 # CSS and JS (includes vendored ApexCharts)
│   ├── templates/               # Base templates
│   └── tests/                  # pytest tests (unit/ and integration/)
├── ml/                         # Similar-incident detection
│   ├── similarity.ipynb        # Model training (TF-IDF)
│   ├── similarity.joblib       # Trained vectorizer, generated by the notebook
│   └── similarity.py           # Inference, imported from src/incidents
├── networking/                 # End-to-end operability check
│   ├── app.py                  # Flask microservice (make run-api)
│   └── check_api.py            # Reads a random incident (sqlite3, no ORM)
├── analysis/
│   └── analysis.ipynb          # Exploratory data analysis with Pandas
├── dashboard/
│   └── dashboard.ipynb         # Complementary dashboard with Matplotlib
├── Makefile
├── pyproject.toml
├── .env.example
└── LICENSE
```

`ml/`, `networking/`, `analysis/` and `dashboard/` deliberately live
outside `src/`: only `ml/similarity.py` is imported from Django (for
similarity inference); everything else is either an analysis notebook or
the Flask microservice, which is queried over HTTP directly from the
browser, never from Python.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/Tenvid/it-incidents-reporter.git
cd it-incidents-reporter

make venv                            # creates the virtual env and installs deps with uv
cp .env.example .env                 # adjust host/port if needed

make migrate                         # applies migrations
uv run python src/manage.py createsuperuser   # needed for the admin dashboard

make seed                            # sample incidents (ARGS="--count 150 --seed 42")
```

To use the "Check dupes" button, generate the similarity model
(`ml/similarity.joblib`, not versioned) by running the `ml/similarity.ipynb`
notebook from the repository root; the database needs incidents for that
(`make seed`). Without the model, the rest of the application works normally.

## Running the project

The operability check (`incidents:operability`) needs **two processes at
once**: Django and the Flask microservice. They can be run separately:

```bash
make run       # Django, http://localhost:8000
make run-api   # Flask, http://localhost:5001 (default)
```

Or both at once:

```bash
make run-all   # both at once, in a single terminal (Ctrl+C stops both)
```

## Tests and code quality

```bash
make test               # all tests (src/tests/)
make test-unit          # unit tests only (src/tests/unit)
make test-integration   # integration tests only (src/tests/integration)

make qa PATH_ARG=incidents   # ruff check + mypy on src/incidents (always includes ml/ and networking/)
```

Integration tests use an in-memory SQLite database, never `db.sqlite3`.

## Technical documentation

Documentation is generated with `pdoc` from the PEP 257 docstrings of
`src/incidents`, `src/user` and `src/incidents_reporter`, into `docs/`
(not version-controlled):

```bash
make docs
```

## Machine Learning model

Training the TF-IDF vectorizer lives in a notebook
(`ml/similarity.ipynb`); only the vectorizer is serialized
(`ml/similarity.joblib`) with `joblib`, since candidate incidents change
constantly and are vectorized on every query. `ml/similarity.py` loads
the vectorizer and performs inference from Django, without retraining on
every request.

## Complementary notebooks

`analysis/analysis.ipynb` (exploratory analysis with Pandas) and
`dashboard/dashboard.ipynb` (charts with Matplotlib) are complementary
features not imported from Django: they read `src/db.sqlite3` in
read-only mode and run from the repository root. The notebook's dashboard
is a separate artifact, independent from the dashboard integrated in
`incidents:dashboard`.

## License

Distributed under the [MIT](LICENSE) license.

## Author

**David Gómez Barberá**

- LinkedIn: [david-gomez-barbera](https://www.linkedin.com/in/david-gomez-barbera/)
- Email: [davidgb.business@gmail.com](mailto:davidgb.business@gmail.com)
