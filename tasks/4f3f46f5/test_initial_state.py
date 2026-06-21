# test_initial_state.py
#
# Pytest suite that verifies the initial operating-system / filesystem state
# before the student performs any actions for the “help-desk tickets” task.
#
# Expectations (truth):
#   • /home/user/tickets.json          – must exist and contain 4 specific tickets.
#   • /home/user/ticket_schema.json    – must exist and contain the exact JSON-Schema
#                                        stipulated in the task description.
#
# NOTE:  We deliberately do NOT check for the presence (or absence) of any output
#        artefacts such as /home/user/validation.log or
#        /home/user/open_network_tickets.json, as mandated by the authoring rules.
#
# The tests use only the Python standard library + pytest.

import json
from pathlib import Path

import pytest

TICKETS_PATH = Path("/home/user/tickets.json")
SCHEMA_PATH = Path("/home/user/ticket_schema.json")


@pytest.fixture(scope="session")
def tickets():
    """Load and return the tickets JSON content."""
    try:
        with TICKETS_PATH.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Required file not found: {TICKETS_PATH}")
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{TICKETS_PATH} is not valid JSON: {exc}")
    return data


@pytest.fixture(scope="session")
def schema():
    """Load and return the ticket JSON-Schema content."""
    try:
        with SCHEMA_PATH.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Required file not found: {SCHEMA_PATH}")
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{SCHEMA_PATH} is not valid JSON: {exc}")
    return data


def test_required_files_exist():
    """Both source JSON files must be present before the student starts."""
    assert TICKETS_PATH.is_file(), f"Missing required file: {TICKETS_PATH}"
    assert SCHEMA_PATH.is_file(), f"Missing required file: {SCHEMA_PATH}"


def test_tickets_json_content(tickets):
    """
    /home/user/tickets.json must contain exactly the four tickets supplied in
    the task description with the correct field values and types.
    """
    expected_tickets = [
        {
            "id": 1001,
            "title": "Router reboot required",
            "status": "open",
            "team": "network",
        },
        {
            "id": 1002,
            "title": "Email account locked",
            "status": "closed",
            "team": "support",
        },
        {
            "id": 1003,
            "title": "Switch firmware upgrade",
            "status": "open",
            "team": "network",
        },
        {
            "id": 1004,
            "title": "Printer not responding",
            "status": "open",
            "team": "support",
        },
    ]

    # Basic structural checks.
    assert isinstance(
        tickets, list
    ), "tickets.json must be a JSON array at the top level."
    assert (
        len(tickets) == 4
    ), f"tickets.json should contain 4 tickets, found {len(tickets)}."

    # Enforce the exact content, ignoring ordering within the list.
    def canonicalise(ticket_dict):
        """Return a tuple representation to allow unordered comparison."""
        return (
            ticket_dict.get("id"),
            ticket_dict.get("title"),
            ticket_dict.get("status"),
            ticket_dict.get("team"),
        )

    assert {canonicalise(t) for t in tickets} == {
        canonicalise(t) for t in expected_tickets
    }, "tickets.json does not contain the expected ticket entries."

    # Type validation for each ticket (simple pass-through without jsonschema).
    for idx, ticket in enumerate(tickets, 1):
        assert isinstance(
            ticket, dict
        ), f"Ticket #{idx} should be a JSON object, got {type(ticket).__name__}."
        for field in ("id", "title", "status", "team"):
            assert (
                field in ticket
            ), f"Ticket #{idx} is missing required field '{field}'."
        assert isinstance(
            ticket["id"], int
        ), f"Ticket #{idx} field 'id' must be integer."
        for field in ("title", "status", "team"):
            assert isinstance(
                ticket[field], str
            ), f"Ticket #{idx} field '{field}' must be string."


def test_ticket_schema_content(schema):
    """
    /home/user/ticket_schema.json must match the schema laid out in the task
    description exactly.
    """
    expected_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["id", "title", "status", "team"],
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "status": {"type": "string"},
                "team": {"type": "string"},
            },
        },
    }

    assert (
        schema == expected_schema
    ), "ticket_schema.json does not match the expected schema definition."