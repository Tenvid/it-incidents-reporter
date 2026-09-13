"""Unit tests for IncidentForm."""

from incidents.forms import IncidentForm

VALID_DATA = {
    "title": "Network outage",
    "description": "No connectivity in building B.",
    "equipment": "Switch-12",
    "priority": "high",
    "status": "open",
}


def test_valid_data_is_valid() -> None:
    form = IncidentForm(data=VALID_DATA)
    assert form.is_valid()


def test_missing_title_is_invalid() -> None:
    data = {**VALID_DATA, "title": ""}
    form = IncidentForm(data=data)
    assert not form.is_valid()
    assert "title" in form.errors


def test_missing_description_is_invalid() -> None:
    data = {**VALID_DATA, "description": ""}
    form = IncidentForm(data=data)
    assert not form.is_valid()
    assert "description" in form.errors


def test_missing_equipment_is_invalid() -> None:
    data = {**VALID_DATA, "equipment": ""}
    form = IncidentForm(data=data)
    assert not form.is_valid()
    assert "equipment" in form.errors


def test_invalid_priority_choice_is_invalid() -> None:
    data = {**VALID_DATA, "priority": "urgent"}
    form = IncidentForm(data=data)
    assert not form.is_valid()
    assert "priority" in form.errors


def test_invalid_status_choice_is_invalid() -> None:
    data = {**VALID_DATA, "status": "resolved"}
    form = IncidentForm(data=data)
    assert not form.is_valid()
    assert "status" in form.errors


def test_title_max_length_boundary_valid() -> None:
    data = {**VALID_DATA, "title": "x" * 200}
    form = IncidentForm(data=data)
    assert form.is_valid()


def test_title_over_max_length_is_invalid() -> None:
    data = {**VALID_DATA, "title": "x" * 201}
    form = IncidentForm(data=data)
    assert not form.is_valid()
    assert "title" in form.errors


def test_equipment_max_length_boundary_valid() -> None:
    data = {**VALID_DATA, "equipment": "x" * 150}
    form = IncidentForm(data=data)
    assert form.is_valid()


def test_equipment_over_max_length_is_invalid() -> None:
    data = {**VALID_DATA, "equipment": "x" * 151}
    form = IncidentForm(data=data)
    assert not form.is_valid()
    assert "equipment" in form.errors


def test_form_excludes_user_and_date_fields() -> None:
    form = IncidentForm()
    assert set(form.fields) == {"title", "description", "equipment", "priority", "status"}
