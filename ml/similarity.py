"""Inference-time similarity scoring for incident duplicate detection.

This module loads the ``TfidfVectorizer`` trained and serialized by
``ml/similarity.ipynb`` and uses it to score a candidate incident's text
against a pool of existing incidents, without ever refitting the vectorizer.
It is imported both by that notebook (for the shared ``build_text`` helper)
and by the ``incidents`` Django app (for inference), and therefore has no
Django dependency of its own.
"""

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import joblib
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = Path(__file__).resolve().parent / "similarity.joblib"
MIN_SCORE = 0.3

VECTORIZER = joblib.load(MODEL_PATH)


def build_text(title: str, description: str, equipment: str) -> str:
    """Join an incident's text fields into the single string the model works on.

    :param title: The incident's title.
    :param description: The incident's description.
    :param equipment: The affected equipment or service.
    :return: The trimmed, non-empty parts joined by a single space.
    """
    parts = (title, description, equipment)
    return " ".join(part.strip() for part in parts if part and part.strip())


def find_similar(
    title: str,
    description: str,
    equipment: str,
    candidates: Sequence[Mapping[str, Any]],
    *,
    min_score: float = MIN_SCORE,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Return the candidates most similar to the given incident text.

    :param title: The title of the incident being checked.
    :param description: The description of the incident being checked.
    :param equipment: The affected equipment or service of the incident being checked.
    :param candidates: Candidate incidents to score against, each a dict with at
        least ``title``, ``description`` and ``equipment`` keys.
    :param min_score: The minimum cosine similarity score to be considered a match.
    :param limit: The maximum number of matches to return.
    :return: The matching candidates, each with an added ``"score"`` key,
        sorted by descending score.
    """
    query_text = build_text(title, description, equipment)
    if not query_text or not candidates:
        return []

    candidate_texts = [
        build_text(candidate["title"], candidate["description"], candidate["equipment"])
        for candidate in candidates
    ]
    candidate_matrix = VECTORIZER.transform(candidate_texts)
    query_vector = VECTORIZER.transform([query_text])
    scores = cosine_similarity(query_vector, candidate_matrix)[0]

    matches = [
        {**candidate, "score": float(score)}
        for candidate, score in zip(candidates, scores, strict=True)
        if score >= min_score
    ]
    matches.sort(key=lambda match: match["score"], reverse=True)
    return matches[:limit]
