"""Standalone Flask service that exposes the operability-check endpoint.

Run directly (``python networking/app.py`` / ``make run-api``), not via the
``flask`` CLI, so this loads its own ``.env`` file explicitly instead of
relying on Flask's CLI-only dotenv support.
"""

import os

from check_api import get_random_incident
from dotenv import load_dotenv
from flask import Flask, Response, jsonify

load_dotenv()

app = Flask(__name__)
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "http://localhost:8000")


@app.after_request
def add_cors_header(response: Response) -> Response:
    """Allow the configured Django origin to read this service's responses.

    :param response: The outgoing Flask response.
    :return: The same response with an ``Access-Control-Allow-Origin``
        header set. A manual header is enough here (no ``flask-cors``
        dependency needed) because the browser only ever issues simple GET
        requests against this service, which never trigger a CORS preflight.
    """
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    return response


@app.get("/random-incident")
def random_incident() -> tuple[Response, int] | Response:
    """Return a random open incident, or a 404 if none are eligible.

    :return: A JSON response with the incident, or a 404 JSON error.
    """
    incident = get_random_incident()
    if incident is None:
        return jsonify({"error": "no incidents available"}), 404
    return jsonify(incident)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("API_HOST", "0.0.0.0"),
        port=int(os.environ.get("API_PORT", "5001")),
    )
