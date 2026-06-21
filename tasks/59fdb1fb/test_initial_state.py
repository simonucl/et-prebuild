# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem state
# BEFORE the learner carries out any actions for the “Nginx compliance
# patch” exercise.
#
# These tests purposefully avoid checking for *output* artefacts such as
# the compliance_patches directory, patch files, backups, logs, etc.
# Only the pre-existing baseline and reference files/directories are
# inspected.

from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constant paths
# ---------------------------------------------------------------------------
HOME = Path("/home/user")
BASELINE_DIR = HOME / "baseline_configs"
SECURE_DIR = HOME / "secure_templates"

BASELINE_FILE = BASELINE_DIR / "nginx.conf"
SECURE_FILE = SECURE_DIR / "nginx.conf"

# ---------------------------------------------------------------------------
# Expected file contents (each ends with a single newline)
# ---------------------------------------------------------------------------
EXPECTED_BASELINE_CONTENT = (
    "worker_processes  1;\n"
    "events {\n"
    "    worker_connections  1024;\n"
    "}\n"
    "\n"
    "http {\n"
    "    server_tokens on;\n"
    "    include       mime.types;\n"
    "    default_type  application/octet-stream;\n"
    "    sendfile        on;\n"
    "    keepalive_timeout  65;\n"
    "}\n"
)

EXPECTED_SECURE_CONTENT = (
    "worker_processes  auto;\n"
    "events {\n"
    "    worker_connections  2048;\n"
    "}\n"
    "\n"
    "http {\n"
    "    server_tokens off;\n"
    "    include       mime.types;\n"
    "    default_type  application/octet-stream;\n"
    "    sendfile        on;\n"
    "    keepalive_timeout  30;\n"
    "    add_header X-Content-Type-Options nosniff;\n"
    "}\n"
)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def read_text(path: Path) -> str:
    """
    Read a file as UTF-8 text.
    A helpful assertion message is provided if the file is missing.
    """
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Could not decode {path} as UTF-8: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_required_directories_exist():
    """baseline_configs/ and secure_templates/ must exist and be directories."""
    assert BASELINE_DIR.exists(), f"Directory {BASELINE_DIR} is missing."
    assert BASELINE_DIR.is_dir(), f"{BASELINE_DIR} exists but is not a directory."

    assert SECURE_DIR.exists(), f"Directory {SECURE_DIR} is missing."
    assert SECURE_DIR.is_dir(), f"{SECURE_DIR} exists but is not a directory."


def test_baseline_file_content_is_as_expected():
    """The baseline nginx.conf must contain the insecure (pre-patch) configuration."""
    content = read_text(BASELINE_FILE)
    assert (
        content == EXPECTED_BASELINE_CONTENT
    ), (
        f"Unexpected contents in {BASELINE_FILE}. "
        "It should match the insecure reference before the exercise begins."
    )


def test_secure_template_content_is_as_expected():
    """The secure template must contain the hardened configuration."""
    content = read_text(SECURE_FILE)
    assert (
        content == EXPECTED_SECURE_CONTENT
    ), (
        f"Unexpected contents in {SECURE_FILE}. "
        "It should match the hardened reference supplied to the learner."
    )


def test_baseline_and_secure_files_differ():
    """Sanity-check: baseline and secure files must differ so that a patch makes sense."""
    baseline = read_text(BASELINE_FILE)
    secure = read_text(SECURE_FILE)
    assert (
        baseline != secure
    ), (
        "The baseline and secure template files are identical; "
        "there would be nothing to patch. Verify the setup fixtures."
    )