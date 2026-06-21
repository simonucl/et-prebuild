# test_initial_state.py
#
# This test-suite verifies that the container starts in a **clean** state
# before the student performs any actions.  It purposefully checks that the
# expected “final” artefacts do *not* yet exist, so the learner can create
# them as part of the assignment.
#
# All tests operate exclusively inside the user’s home directory
# (/home/user) and rely only on the Python standard library and pytest.

import os
from pathlib import Path

HOME = Path("/home/user")
BASHRC = HOME / ".bashrc"
OBSERVABILITY_DIR = HOME / "observability"
CUSTOM_INI = OBSERVABILITY_DIR / "custom.ini"
VALIDATION_LOG = OBSERVABILITY_DIR / "setup_time_locale.log"

TZ_LINE = 'export TZ="America/New_York"'
LANG_LINE = 'export LANG="en_US.UTF-8"'
LC_ALL_LINE = 'export LC_ALL="en_US.UTF-8"'
DONE_MARKER = "# <<< locale-tz-setup-done >>>"

TZ_KV = "default_timezone = America/New_York"
LANG_KV = "default_language = en_US.UTF-8"


def _read_text_lines(path: Path):
    """Utility: read file and return list of stripped lines; empty list on missing path."""
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []


def test_bashrc_does_not_yet_contain_export_lines():
    """
    The three export lines must NOT be present before the student touches the file.
    If ~/.bashrc does not exist yet, that is also acceptable.
    """
    if not BASHRC.exists():
        # A missing file is fine for the initial state.
        return

    lines = [ln.strip() for ln in _read_text_lines(BASHRC)]

    assert TZ_LINE not in lines, (
        f"{BASHRC} already contains the timezone export line — "
        "this should be added by the student, not pre-exist."
    )
    assert LANG_LINE not in lines, (
        f"{BASHRC} already contains the LANG export line — "
        "this should be added by the student."
    )
    assert LC_ALL_LINE not in lines, (
        f"{BASHRC} already contains the LC_ALL export line — "
        "this should be added by the student."
    )


def test_bashrc_last_line_is_not_done_marker():
    """
    The special marker must *not* yet be the last line; it will be appended
    only after the student completes the task.
    """
    if not BASHRC.exists():
        return

    lines = _read_text_lines(BASHRC)
    if not lines:
        return

    assert lines[-1].strip() != DONE_MARKER, (
        f"The last line of {BASHRC} is already the completion marker "
        f'({DONE_MARKER!r}).  The file should start without it.'
    )


def test_custom_ini_not_fully_configured_yet():
    """
    Either the Grafana custom.ini is absent or, if present, it must not
    already contain BOTH of the required key/value pairs.
    """
    if not CUSTOM_INI.exists():
        # Missing file is fine at this point.
        return

    lines = [ln.strip() for ln in _read_text_lines(CUSTOM_INI)]
    has_tz_kv = TZ_KV in lines
    has_lang_kv = LANG_KV in lines

    assert not (has_tz_kv and has_lang_kv), (
        f"{CUSTOM_INI} already contains both required configuration lines; "
        "the student should add them during the exercise."
    )


def test_validation_log_not_present():
    """
    The validation log file must not exist before the student creates it.
    """
    assert not VALIDATION_LOG.exists(), (
        f"{VALIDATION_LOG} already exists — the student is expected to create "
        "this log file as part of the assignment."
    )