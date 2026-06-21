# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state *before* the student executes any action.
#
# Checks performed:
#   1. The docker-compose file exists at the expected absolute path.
#   2. The compose file contains the two required services—prometheus
#      and grafana—in that order.
#
# NOTE: Per the grading specification we intentionally DO NOT reference,
#       check for, or expect the yet-to-be-created
#       /home/user/projects/metrics/defined_services.log file.

import os
import re
from pathlib import Path

import pytest

COMPOSE_PATH = Path("/home/user/projects/metrics/docker-compose.yml")


def read_compose_lines():
    """
    Helper that returns the docker-compose file as a list of stripped lines.

    Raises:
        pytest.SkipTest: if the compose file is missing so that downstream
        tests fail with a single clear message.
    """
    if not COMPOSE_PATH.is_file():
        pytest.skip(
            f"Required compose file not found at {COMPOSE_PATH}. "
            "Create it before proceeding."
        )
    with COMPOSE_PATH.open(encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


def test_compose_file_exists():
    """
    Ensure the docker-compose file is present.
    """
    assert COMPOSE_PATH.is_file(), (
        f"Expected docker-compose file missing at {COMPOSE_PATH}. "
        "Create the file before attempting the exercise."
    )


def test_compose_contains_services_in_order():
    """
    Verify that the compose file defines the 'prometheus' and 'grafana'
    services, in that order, beneath the 'services:' key.
    """
    lines = read_compose_lines()

    # Locate the 'services:' section.
    try:
        services_idx = next(
            idx for idx, ln in enumerate(lines)
            if re.fullmatch(r"\s*services:\s*", ln)
        )
    except StopIteration:  # pragma: no cover
        pytest.fail(
            f"'services:' section not found in {COMPOSE_PATH}. "
            "Ensure the compose file follows standard format."
        )

    # From the line after 'services:', search for the two service names.
    prometheus_idx = grafana_idx = None
    for idx in range(services_idx + 1, len(lines)):
        ln = lines[idx]
        if prometheus_idx is None and re.fullmatch(r"\s*prometheus:\s*", ln):
            prometheus_idx = idx
        if prometheus_idx is not None and re.fullmatch(r"\s*grafana:\s*", ln):
            grafana_idx = idx
            break  # Order found, can exit early.

    if prometheus_idx is None:
        pytest.fail(
            "Service 'prometheus' not declared under the 'services:' section "
            f"in {COMPOSE_PATH}. Add it before proceeding."
        )

    if grafana_idx is None:
        pytest.fail(
            "Service 'grafana' not declared under the 'services:' section "
            f"in {COMPOSE_PATH}. Add it before proceeding."
        )

    assert prometheus_idx < grafana_idx, (
        "Services are not in the required order: 'prometheus' must appear "
        "before 'grafana' inside the compose file."
    )