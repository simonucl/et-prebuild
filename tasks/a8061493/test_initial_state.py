# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student starts making any changes.  It makes sure that
# the configuration files contain the original values and that the
# expected directories already exist.
#
# NOTE:
# • We intentionally do *not* check for the presence or absence of any
#   future output artefacts (e.g., optimization.log) in order to comply
#   with the grading-rules.

from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/projects/cloud-cost-optimizer")
CFG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"

THRESHOLDS_FILE = CFG_DIR / "thresholds.yml"
ALERTS_FILE = CFG_DIR / "alerts.toml"

EXPECTED_THRESHOLDS = (
    "aws:\n"
    "  monthly_budget: 7000\n"
    "  alert_at_percent: 90\n"
    "azure:\n"
    "  monthly_budget: 5000\n"
    "  alert_at_percent: 90\n"
    "gcp:\n"
    "  monthly_budget: 4000\n"
    "  alert_at_percent: 90\n"
)

EXPECTED_ALERTS = (
    "[email]\n"
    'recipients = ["finops@example.com","cloudteam@example.com"]\n'
)


def _read_file(path: Path) -> str:
    """
    Helper that returns the *raw* contents of a file.

    The function strips a single trailing newline so that we can compare
    files regardless of whether the author left an extra newline at EOF.
    """
    data = path.read_text(encoding="utf-8")
    return data.rstrip("\n")


@pytest.mark.describe("Filesystem pre-check")
class TestInitialState:
    def test_directories_exist(self):
        assert CFG_DIR.is_dir(), (
            f"Expected configuration directory to exist at '{CFG_DIR}'."
        )
        assert LOGS_DIR.is_dir(), (
            f"Expected logs directory to exist at '{LOGS_DIR}'."
        )

    def test_thresholds_yml_initial_content(self):
        assert THRESHOLDS_FILE.is_file(), (
            f"File '{THRESHOLDS_FILE}' is missing."
        )
        actual = _read_file(THRESHOLDS_FILE)
        expected = EXPECTED_THRESHOLDS.rstrip("\n")
        assert actual == expected, (
            f"'{THRESHOLDS_FILE}' does not contain the expected initial "
            "threshold values.\n\n"
            "Expected:\n"
            f"{EXPECTED_THRESHOLDS!r}\n\n"
            "Found:\n"
            f"{actual!r}"
        )

    def test_alerts_toml_initial_content(self):
        assert ALERTS_FILE.is_file(), (
            f"File '{ALERTS_FILE}' is missing."
        )
        actual = _read_file(ALERTS_FILE)
        expected = EXPECTED_ALERTS.rstrip("\n")
        assert actual == expected, (
            f"'{ALERTS_FILE}' should only contain the initial [email] table "
            "before the task starts.\n\n"
            "Expected:\n"
            f"{EXPECTED_ALERTS!r}\n\n"
            "Found:\n"
            f"{actual!r}"
        )