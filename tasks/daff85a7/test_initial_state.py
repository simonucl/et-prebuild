# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem
state before the student starts working on the exercise.

Rules:
* Only stdlib + pytest are used.
* We purposely do NOT test for the presence (or absence) of any artefacts
  that the student must create (/home/user/incidents, etc.).
* We *do* verify that the source HTML file provided to the student exists
  and contains the expected structural markers so subsequent tests can rely
  on it being well-formed.
"""

import os
import re
from pathlib import Path

STATUS_HTML = Path("/home/user/internal_status/status.html")


def test_status_html_exists_and_is_readable():
    """Ensure the source HTML snapshot exists and is readable."""
    assert STATUS_HTML.exists(), (
        f"Required file {STATUS_HTML} is missing.  It should have been "
        "pre-placed for the student."
    )
    assert STATUS_HTML.is_file(), f"{STATUS_HTML} exists but is not a regular file."
    # Check read permissions by trying to open it.
    try:
        STATUS_HTML.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover – we want any failure
        assert False, f"Unable to read {STATUS_HTML}: {exc}"


def test_status_html_contains_incident_table():
    """
    Sanity-check that the HTML contains a <table id="incidents"> with at
    least one <tr> inside its <tbody>.  This guarantees the downstream
    scraping logic has something to work with.
    """
    html = STATUS_HTML.read_text(encoding="utf-8")

    # 1. <table id="incidents"> must exist
    table_pattern = re.compile(r'<table[^>]*\bid\s*=\s*["\']incidents["\']', re.I)
    assert table_pattern.search(html), (
        f"{STATUS_HTML} does not contain a table with id='incidents'.  "
        "The scraping task requires this precise element."
    )

    # 2. Ensure there is a <tbody> section
    tbody_match = re.search(r"<tbody>(.*?)</tbody>", html, re.I | re.S)
    assert tbody_match, (
        f"{STATUS_HTML} lacks a <tbody> section inside the incidents table."
    )

    # 3. Verify at least one <tr> row inside <tbody>
    rows = re.findall(r"<tr>(.*?)</tr>", tbody_match.group(1), re.I | re.S)
    assert rows, (
        f"The <tbody> inside the incidents table has no <tr> rows.  "
        "At least one incident row is required for the exercise."
    )