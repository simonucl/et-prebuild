# test_initial_state.py
#
# Pytest suite that validates the machine **before** the student starts working.
# The tests make sure the prescribed initial filesystem state really exists and
# that no “solution” artefacts are already present.

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants                                                                   
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
LOG_DIR = HOME / "server_logs"
LOG_FILE = LOG_DIR / "app.log"
ANALYSIS_DIR = HOME / "analysis"          # Must NOT exist yet

# Exact, byte–for–byte contents that must be present in app.log
EXPECTED_LOG_TEXT = (
    "2023-04-29 11:22:33 [INFO]  (192.168.1.10) status=200 Request processed successfully\n"
    "2023-04-29 11:22:34 [ERROR] (192.168.1.11) status=500 Internal server error\n"
    "2023-04-29 11:22:35 [WARN]  (192.168.1.12) status=404 Resource not found\n"
    "2023-04-29 11:22:36 [ERROR] (10.0.0.5)     status=503 Service unavailable\n"
    "2023-04-29 11:22:37 [INFO]  (192.168.1.10) status=200 Request processed successfully\n"
    "2023-04-29 11:22:38 [ERROR] (172.16.0.2)   status=501 Not implemented\n"
    "2023-04-29 11:22:39 [INFO]  (192.168.1.15) status=302 Redirect\n"
    "2023-04-29 11:22:40 [ERROR] (192.168.1.11) status=500 Internal server error\n"
    "2023-04-29 11:22:41 [INFO]  (192.168.1.10) status=200 Request processed successfully\n"
    "2023-04-29 11:22:42 [ERROR] (10.0.0.5)     status=504 Gateway timeout\n"
)

# --------------------------------------------------------------------------- #
# Helper functions                                                            
# --------------------------------------------------------------------------- #

def read_file(path: Path) -> str:
    """Return the full text of *path* as UTF-8. Fail early if it cannot be read."""
    assert path.exists(), f"Required file is missing: {path}"
    assert path.is_file(), f"Expected a regular file but found something else: {path}"
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()

# --------------------------------------------------------------------------- #
# Tests                                                                       
# --------------------------------------------------------------------------- #

def test_log_directory_exists():
    assert LOG_DIR.exists(), f"Log directory is missing: {LOG_DIR}"
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."

def test_app_log_exists_and_has_correct_contents():
    assert LOG_FILE.exists(), f"Log file is missing: {LOG_FILE}"
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."

    actual = read_file(LOG_FILE)
    assert actual == EXPECTED_LOG_TEXT, (
        "Contents of /home/user/server_logs/app.log do not match the expected "
        "initial data. The file must remain unmodified until the student "
        "creates the solution artefacts."
    )

def test_no_extra_files_in_log_directory():
    files = sorted(p.name for p in LOG_DIR.iterdir() if p.is_file())
    assert files == ["app.log"], (
        f"The log directory {LOG_DIR} must contain exactly one file called "
        f"'app.log'. Current contents: {files}"
    )

def test_analysis_directory_absent():
    assert not ANALYSIS_DIR.exists(), (
        f"The analysis directory {ANALYSIS_DIR} should NOT exist before the "
        f"student runs their solution."
    )