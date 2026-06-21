# test_initial_state.py
# ---------------------
# A pytest test-suite that validates the **initial** operating-system /
# file-system state before the student runs any code.  It intentionally
# checks only the pre-existing artefacts mentioned in the task description
# (the HTML sources under /home/user/releases/) and deliberately ignores
# any of the expected *output* files or directories.
#
# If any assertion here fails, the accompanying message pin-points the
# exact discrepancy so that the student immediately knows what is missing
# or differs from the canonical starting point.

import os
from pathlib import Path

RELEASE_DIR = Path("/home/user/releases")

# These are the files that *must* exist – no more, no fewer.
EXPECTED_FILES = {
    "auth-service.html",
    "payment-service.html",
    "notification-service.html",
}

# Canonical file contents – including exact whitespace and the required
# trailing newline.  Any deviation (extra spaces, different line-breaks,
# missing newline at EOF, etc.) will make the assertion fail.
AUTH_EXPECTED = """<!DOCTYPE html>
<html>
<head><title>Auth Service Releases</title></head>
<body>
    <h1>Auth Service</h1>
    <div class="latest-release">
        <span class="version">v1.8.3</span>
        <span class="released">2023-07-18</span>
    </div>
    <div class="latest-release">
        <span class="version">v1.8.2</span>
        <span class="released">2023-06-02</span>
    </div>
</body>
</html>
"""

PAYMENT_EXPECTED = """<!DOCTYPE html>
<html>
<head><title>Payment Service Releases</title></head>
<body>
    <h1>Payment Service</h1>
    <div class="latest-release">
        <span class="version">v3.2.0</span>
        <span class="released">2023-07-20</span>
    </div>
    <div class="latest-release">
        <span class="version">v3.1.4</span>
        <span class="released">2023-05-15</span>
    </div>
</body>
</html>
"""

NOTIFICATION_EXPECTED = """<!DOCTYPE html>
<html>
<head><title>Notification Service Releases</title></head>
<body>
    <h1>Notification Service</h1>
    <div class="latest-release">
        <span class="version">v2.0.5</span>
        <span class="released">2023-07-21</span>
    </div>
    <div class="latest-release">
        <span class="version">v2.0.4</span>
        <span class="released">2023-06-30</span>
    </div>
</body>
</html>
"""


def test_releases_directory_exists():
    assert RELEASE_DIR.exists(), f"Required directory {RELEASE_DIR} is missing."
    assert RELEASE_DIR.is_dir(), f"{RELEASE_DIR} exists but is not a directory."


def test_releases_directory_has_expected_files_only():
    present = {p.name for p in RELEASE_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_FILES - present
    extra = present - EXPECTED_FILES
    assert not missing, (
        "The following required files are missing from "
        f"{RELEASE_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected files present in {RELEASE_DIR}: "
        f"{', '.join(sorted(extra))}. The directory should contain *only* "
        "the three service HTML pages."
    )


def _read(path: Path) -> str:
    """
    Read file using universal newlines so that different newline encodings
    ('\\n', '\\r\\n') normalise to '\\n'.  This keeps the comparison strict
    but platform-agnostic.
    """
    with path.open("r", newline=None) as fp:
        return fp.read()


def test_auth_service_html_content_matches_canonical():
    path = RELEASE_DIR / "auth-service.html"
    assert path.exists(), f"{path} is missing."
    assert _read(path) == AUTH_EXPECTED, (
        f"Contents of {path} differ from the expected canonical HTML. "
        "Ensure the file is unmodified and matches exactly."
    )


def test_payment_service_html_content_matches_canonical():
    path = RELEASE_DIR / "payment-service.html"
    assert path.exists(), f"{path} is missing."
    assert _read(path) == PAYMENT_EXPECTED, (
        f"Contents of {path} differ from the expected canonical HTML."
    )


def test_notification_service_html_content_matches_canonical():
    path = RELEASE_DIR / "notification-service.html"
    assert path.exists(), f"{path} is missing."
    assert _read(path) == NOTIFICATION_EXPECTED, (
        f"Contents of {path} differ from the expected canonical HTML."
    )