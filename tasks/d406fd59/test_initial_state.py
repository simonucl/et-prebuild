# test_initial_state.py
#
# This pytest suite validates that the machine is still in its **initial**
# state, _before_ the student performs any of the required edits.
#
# It checks:
#   1. Exact contents of /home/user/logtool/config/settings.yaml
#   2. Exact contents of /home/user/logtool/config/filters.toml
#   3. Presence of /home/user/logtool/output/ **and** that it is empty
#   4. Absence of /home/user/logtool/output/pattern_summary.log
#
# If any of these assertions fail, the error message pinpoints what is
# missing or unexpected.

import os
import textwrap
import pytest


# ---------- Constants with the expected initial file contents ----------
EXPECTED_SETTINGS_YAML = textwrap.dedent(
    """\
    # LogTool configuration
    alert_threshold: 90
    pattern_detection: false
    log_paths:
      - /var/log/syslog
      - /var/log/auth.log
    """
)

EXPECTED_FILTERS_TOML = textwrap.dedent(
    """\
    # Default filter rules
    [[rules]]
    name = "ignore_health_checks"
    pattern = "healthcheck"
    action = "drop"
    """
)


# ---------- Helper utilities ----------
def _normalized_file_contents(path: str) -> str:
    """
    Read a file and normalise its UNIX newline endings.  This helps us make
    strictly byte-for-byte comparisons, while still tolerating the presence
    or absence of a trailing newline at EOF.
    """
    with open(path, "r", encoding="utf-8") as fp:
        contents = fp.read()

    # Ensure all line endings are LF and the file ends with exactly one \n.
    contents = contents.replace("\r\n", "\n").replace("\r", "\n")
    if not contents.endswith("\n"):
        contents += "\n"
    return contents


# ---------- Tests ----------
def test_settings_yaml_initial_state():
    path = "/home/user/logtool/config/settings.yaml"
    assert os.path.isfile(path), f"Expected config file missing: {path}"

    actual = _normalized_file_contents(path)
    expected = EXPECTED_SETTINGS_YAML
    assert (
        actual == expected
    ), (
        f"Unexpected contents in {path}.\n"
        "---- Expected ----\n"
        f"{expected}---- Got ----\n{actual}"
    )


def test_filters_toml_initial_state():
    path = "/home/user/logtool/config/filters.toml"
    assert os.path.isfile(path), f"Expected config file missing: {path}"

    actual = _normalized_file_contents(path)
    expected = EXPECTED_FILTERS_TOML
    assert (
        actual == expected
    ), (
        f"Unexpected contents in {path}.\n"
        "---- Expected ----\n"
        f"{expected}---- Got ----\n{actual}"
    )


def test_output_directory_exists_and_empty():
    output_dir = "/home/user/logtool/output"
    assert os.path.isdir(
        output_dir
    ), f"Output directory missing: {output_dir}"

    # List only files (ignore eventual sub-dirs just in case)
    files = [
        entry
        for entry in os.listdir(output_dir)
        if os.path.isfile(os.path.join(output_dir, entry))
    ]
    assert (
        len(files) == 0
    ), f"Output directory {output_dir} is expected to be empty, but contains: {files}"


def test_pattern_summary_log_absent():
    """
    The verification file should NOT exist yet in the initial state.
    """
    summary_log = "/home/user/logtool/output/pattern_summary.log"
    assert not os.path.exists(
        summary_log
    ), f"{summary_log} should not exist before the student makes any changes."