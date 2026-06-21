# test_initial_state.py
#
# This pytest suite verifies that the **initial** operating-system / filesystem
# state is correct _before_ the student performs any action.
#
# It checks for:
#   1. Presence of the report HTML file that advertises an expected SHA-256 hash.
#   2. Presence of the archive that must be verified.
#   3. Correct HTML structure: exactly one <code>…</code> element containing one
#      64-character hexadecimal hash.
#   4. Internal consistency: the advertised hash must *already* match the real
#      SHA-256 checksum of the archive.  (If this were not true, the student
#      would be forced to log “match: false” even with perfect code.)
#
# Nothing about the eventual output file
#   /home/user/backup_checks/verification.log
# is tested here—that is the student’s responsibility.

import hashlib
import os
import re
import pytest

# Absolute paths required by the task description
REPORT_HTML = "/home/user/server/backup_report.html"
ARCHIVE_PATH = "/home/user/data/backup.tar.gz"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
HEX64_RE = re.compile(r"<code>\s*([0-9a-f]{64})\s*</code>", re.IGNORECASE)


def extract_hash_from_html(html_path: str) -> str:
    """Return the single 64-hex-char string inside <code>…</code> tags.

    Raises informative AssertionErrors if the requirements are not met.
    """
    assert os.path.isfile(html_path), (
        f"Expected HTML report not found at: {html_path}"
    )

    with open(html_path, "r", encoding="utf-8") as fp:
        content = fp.read()

    matches = HEX64_RE.findall(content)
    assert matches, (
        "No 64-character hexadecimal hash found inside <code>…</code> tags "
        f"in {html_path}"
    )
    assert len(matches) == 1, (
        f"Expected exactly ONE <code>…</code> element containing a SHA-256 "
        f"hash in {html_path}, but found {len(matches)}."
    )

    return matches[0].lower()


def sha256_of_file(path: str) -> str:
    """Compute and return the SHA-256 hex digest of the given file."""
    assert os.path.isfile(path), f"Archive not found at: {path}"

    hasher = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_report_html_exists():
    """The backup_report.html file must exist."""
    assert os.path.isfile(REPORT_HTML), (
        f"Required report file missing: {REPORT_HTML}"
    )


def test_archive_exists():
    """The backup tarball must exist."""
    assert os.path.isfile(ARCHIVE_PATH), (
        f"Required archive file missing: {ARCHIVE_PATH}"
    )


def test_report_contains_single_sha256():
    """The HTML must contain exactly one valid SHA-256 hex digest in <code> tags."""
    _ = extract_hash_from_html(REPORT_HTML)  # Assertions fire inside helper.


def test_advertised_hash_matches_actual_archive():
    """The hash inside the HTML must already match the real archive checksum."""
    expected_hash = extract_hash_from_html(REPORT_HTML)
    actual_hash = sha256_of_file(ARCHIVE_PATH)

    assert expected_hash == actual_hash, (
        "Mismatch between advertised SHA-256 in the HTML report "
        f"({expected_hash}) and the actual SHA-256 of the archive "
        f"({actual_hash}).  The initial environment is inconsistent."
    )