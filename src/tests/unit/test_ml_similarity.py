"""Unit tests for ml/similarity.py."""

from sklearn.feature_extraction.text import TfidfVectorizer

from ml import similarity
from ml.similarity import build_text, find_similar


def test_build_text_joins_all_non_empty_fields() -> None:
    text = build_text("Printer jam", "Paper stuck", "Printer-2F")
    assert text == "Printer jam Paper stuck Printer-2F"


def test_build_text_trims_whitespace() -> None:
    text = build_text("  Printer jam  ", " Paper stuck ", " Printer-2F ")
    assert text == "Printer jam Paper stuck Printer-2F"


def test_build_text_skips_empty_fields() -> None:
    assert build_text("Printer jam", "", "Printer-2F") == "Printer jam Printer-2F"


def test_build_text_returns_empty_string_for_all_empty_fields() -> None:
    assert build_text("", "  ", "") == ""


def test_find_similar_returns_match_above_threshold(fitted_vectorizer: TfidfVectorizer) -> None:
    candidates = [
        {
            "id": 1,
            "title": "Printer jam",
            "description": "printer paper jam display shows error",
            "equipment": "printer room",
        }
    ]
    matches = find_similar(
        "Printer jam", "printer paper jam display shows error", "printer room", candidates
    )
    assert len(matches) == 1
    assert matches[0]["id"] == 1
    assert matches[0]["score"] >= similarity.MIN_SCORE


def test_find_similar_excludes_unrelated_candidate_below_threshold(
    fitted_vectorizer: TfidfVectorizer,
) -> None:
    candidates = [
        {
            "id": 1,
            "title": "Coffee machine",
            "description": "coffee machine leaking water kitchen floor",
            "equipment": "kitchen",
        }
    ]
    matches = find_similar(
        "Printer jam", "printer paper jam display shows error", "printer room", candidates
    )
    assert matches == []


def test_find_similar_returns_empty_list_for_empty_query_text(
    fitted_vectorizer: TfidfVectorizer,
) -> None:
    candidates = [
        {"id": 1, "title": "Printer jam", "description": "printer paper jam", "equipment": "printer room"}
    ]
    assert find_similar("", "", "", candidates) == []


def test_find_similar_returns_empty_list_for_no_candidates(fitted_vectorizer: TfidfVectorizer) -> None:
    assert find_similar("Printer jam", "printer paper jam", "printer room", []) == []


def test_find_similar_limit_caps_number_of_results(fitted_vectorizer: TfidfVectorizer) -> None:
    candidates = [
        {
            "id": i,
            "title": "Printer jam",
            "description": "printer paper jam display shows error",
            "equipment": "printer room",
        }
        for i in range(5)
    ]
    matches = find_similar(
        "Printer jam",
        "printer paper jam display shows error",
        "printer room",
        candidates,
        limit=2,
    )
    assert len(matches) == 2
