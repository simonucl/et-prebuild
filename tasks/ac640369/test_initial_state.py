# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state for the FinOps cost-control exercise.  It should be executed **before**
# the student performs any edits.  If any test fails, the environment is not
# in the expected pristine state and the task instructions will no longer
# apply verbatim.

import os
import stat
import pytest

BASE_DIR = "/home/user/finops"
COST_ALERTS_PATH = os.path.join(BASE_DIR, "cost-alerts.yaml")
BUDGET_PATH = os.path.join(BASE_DIR, "budget.toml")
UPDATE_LOG_PATH = os.path.join(BASE_DIR, "update_log.txt")


@pytest.fixture(scope="module")
def initial_cost_alerts_bytes():
    """
    The exact byte sequence expected for cost-alerts.yaml
    (UTF-8, LF newlines, terminating newline included).
    """
    return (
        b"alerts:\n"
        b"  - name: daily-spend\n"
        b"    threshold: 500\n"
        b"    channels:\n"
        b"      - slack\n"
        b"      - email\n"
        b"  - name: monthly-spend\n"
        b"    threshold: 15000\n"
        b"    channels:\n"
        b"      - slack\n"
    )


@pytest.fixture(scope="module")
def initial_budget_bytes():
    """
    The exact byte sequence expected for budget.toml
    (UTF-8, LF newlines, terminating newline included).
    """
    return (
        b"[budget]\n"
        b"monthly_limit = 20000\n"
        b"daily_limit  = 700\n"
        b"\n"
        b"[metadata]\n"
        b"owner        = \"finops-team\"\n"
        b"last_updated = \"2023-01-15\"\n"
    )


def test_finops_directory_exists_and_permissions():
    assert os.path.isdir(BASE_DIR), (
        f"Required directory {BASE_DIR} is missing. "
        "The exercise must be performed inside this folder."
    )
    mode = os.stat(BASE_DIR).st_mode
    assert mode & stat.S_IRUSR, f"{BASE_DIR} is not readable."
    assert mode & stat.S_IWUSR, f"{BASE_DIR} is not writable by the user."


def test_cost_alerts_initial_contents(initial_cost_alerts_bytes):
    assert os.path.isfile(COST_ALERTS_PATH), (
        f"{COST_ALERTS_PATH} is missing. "
        "The cost-alerts.yaml file must be present before editing."
    )
    with open(COST_ALERTS_PATH, "rb") as fh:
        actual = fh.read()
    assert (
        actual == initial_cost_alerts_bytes
    ), (
        f"{COST_ALERTS_PATH} contents differ from expected pristine state.\n\n"
        "Tips:\n"
        "• Newline style must be LF (\\n).\n"
        "• Indentation is two spaces per level.\n"
        "• File must end with exactly one trailing newline.\n"
    )


def test_budget_initial_contents(initial_budget_bytes):
    assert os.path.isfile(BUDGET_PATH), (
        f"{BUDGET_PATH} is missing. "
        "The budget.toml file must be present before editing."
    )
    with open(BUDGET_PATH, "rb") as fh:
        actual = fh.read()
    assert (
        actual == initial_budget_bytes
    ), (
        f"{BUDGET_PATH} contents differ from expected pristine state.\n\n"
        "Ensure keys, spacing, alignment, and newline characters "
        "match the specification exactly."
    )


def test_update_log_does_not_exist_yet():
    assert not os.path.exists(
        UPDATE_LOG_PATH
    ), (
        f"{UPDATE_LOG_PATH} already exists, but the student has "
        "not yet performed any changes.  The log file must be created "
        "only after the configuration edits are complete."
    )