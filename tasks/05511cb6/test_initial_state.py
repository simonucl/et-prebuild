# test_initial_state.py
#
# This pytest suite validates that the filesystem is in the **initial** state
# expected *before* the student starts working on the incident-log exercise.
# It checks that:
#   • The two seed log files exist and contain the exact, predefined content.
#   • No output artefacts from the yet-to-be-written solution are present.
#
# If any of these assertions fail, the student’s starting environment is
# incorrect and the exercise itself cannot be trusted to run properly.

import pathlib
import textwrap
import pytest

HOME = pathlib.Path("/home/user")

# --------------------------------------------------------------------------- #
# Expected seed log contents                                                   #
# --------------------------------------------------------------------------- #

SEED_15 = textwrap.dedent(
    """\
    2023-07-15 10:12:05,123 [auth] INFO User john@example.com logged in
    2023-07-15 10:13:07,456 [payment] ERROR Failed payment for user jane.doe@example.com: insufficient funds
    2023-07-15 10:15:00,789 [search] WARN Slow query
    2023-07-15 10:16:12,321 [payment] ERROR Timeout contacting bank API
    2023-07-15 10:18:45,654 [auth] ERROR Invalid password for user admin@example.com
    2023-07-15 10:20:11,987 [inventory] INFO Stock updated
    """
)

SEED_16 = textwrap.dedent(
    """\
    2023-07-16 09:01:02,111 [auth] INFO User alice@example.com logged in
    2023-07-16 09:05:33,222 [search] ERROR Null pointer in search index
    2023-07-16 09:10:44,333 [payment] ERROR Currency conversion failed for user bob@example.com
    2023-07-16 09:15:55,444 [auth] WARN Token nearing expiry
    2023-07-16 09:20:06,555 [payment] ERROR Duplicate transaction detected
    2023-07-16 09:25:17,666 [search] ERROR Failed to parse query "foo bar"
    """
)

# Normalise strings to have a single trailing newline exactly
SEED_15 = SEED_15.rstrip("\n") + "\n"
SEED_16 = SEED_16.rstrip("\n") + "\n"


# --------------------------------------------------------------------------- #
# Utility helpers                                                             #
# --------------------------------------------------------------------------- #
def read_file(path: pathlib.Path) -> str:
    try:
        data = path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")
    return data


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_seed_log_files_exist():
    """Both incident-log source files must exist."""
    logs_dir = HOME / "incident_logs"
    assert logs_dir.is_dir(), (
        f"Expected incident log directory {logs_dir} to exist, "
        "but it is missing."
    )

    log15 = logs_dir / "app_2023-07-15.log"
    log16 = logs_dir / "app_2023-07-16.log"

    assert log15.is_file(), f"Missing seed log file: {log15}"
    assert log16.is_file(), f"Missing seed log file: {log16}"


def test_seed_log_contents_are_correct():
    """The seed log files must match the canonical content exactly."""
    logs_dir = HOME / "incident_logs"
    log15 = logs_dir / "app_2023-07-15.log"
    log16 = logs_dir / "app_2023-07-16.log"

    contents15 = read_file(log15)
    contents16 = read_file(log16)

    assert contents15 == SEED_15, (
        f"Contents of {log15} do not match the expected seed data."
    )
    assert contents16 == SEED_16, (
        f"Contents of {log16} do not match the expected seed data."
    )


def test_no_output_files_exist_yet():
    """
    At the start of the exercise the /home/user/output directory should NOT
    already contain the artefacts the student is supposed to create.
    """
    output_dir = HOME / "output"

    # It is fine if the directory already exists (e.g. previous attempts),
    # but none of the required files should be present yet.
    expected_paths = [
        output_dir / "errors_combined.log",
        output_dir / "error_summary.csv",
        output_dir / "incident_report.txt",
    ]

    for path in expected_paths:
        assert not path.exists(), (
            f"The file {path} exists before the exercise has begun. "
            "The starting state must not contain any output artefacts."
        )