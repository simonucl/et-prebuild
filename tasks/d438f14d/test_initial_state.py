# test_initial_state.py
#
# This pytest suite validates the initial operating-system / filesystem
# state **before** the student performs any actions for the FinOps task.
#
# Rules enforced:
#   • /home/user/data/cloudbilling.html must exist.
#   • The file’s contents must match the specification *exactly*,
#     including whitespace and newline characters.
#
# No other files or directories are tested here, as the output artefacts
# (e.g. /home/user/finops/*) do not yet exist at this stage.

from pathlib import Path
import pytest

DATA_DIR = Path("/home/user/data")
HTML_PATH = DATA_DIR / "cloudbilling.html"

# Expected HTML content (trailing newline included).
EXPECTED_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cloud Billing Portal</title>
</head>
<body>
    <h1>Monthly Cost Breakdown</h1>
    <table id="cost-table">
        <thead>
            <tr><th>Service</th><th>Monthly Cost (USD)</th></tr>
        </thead>
        <tbody>
            <tr><td>EC2</td><td>$45.32</td></tr>
            <tr><td>S3</td><td>$12.05</td></tr>
            <tr><td>RDS</td><td>$33.10</td></tr>
        </tbody>
    </table>
</body>
</html>
"""

def test_data_directory_exists():
    """Ensure /home/user/data directory exists and is a directory."""
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."

def test_html_file_exists():
    """Ensure the HTML billing file exists before the exercise begins."""
    assert HTML_PATH.exists(), f"Required file {HTML_PATH} is missing."
    assert HTML_PATH.is_file(), f"{HTML_PATH} exists but is not a regular file."

def test_html_file_contents_exactly_match():
    """
    Verify that /home/user/data/cloudbilling.html contains the exact, 
    byte-for-byte content specified in the exercise preconditions.
    """
    actual = HTML_PATH.read_text(encoding="utf-8")
    if actual != EXPECTED_HTML:
        # Provide a concise diff-like message for easier debugging.
        # Only show the first differing line to avoid overwhelming output.
        expected_lines = EXPECTED_HTML.splitlines(keepends=True)
        actual_lines = actual.splitlines(keepends=True)
        for idx, (e_line, a_line) in enumerate(zip(expected_lines, actual_lines), start=1):
            if e_line != a_line:
                raise AssertionError(
                    f"Content mismatch in {HTML_PATH} at line {idx}.\n"
                    f"Expected: {e_line!r}\n"
                    f"Actual:   {a_line!r}"
                )
        # If we reach here, length differs
        raise AssertionError(
            f"Content length mismatch in {HTML_PATH}. "
            f"Expected {len(EXPECTED_HTML)} bytes, got {len(actual)} bytes."
        )