# test_initial_state.py
#
# pytest suite that verifies the pristine environment *before*
# the student creates any output artefacts.  It checks that:
#   1. The expected three legacy INI files exist – and *only* those –
#      inside /home/user/data/configs.
#   2. The contents of those files match the specification that the
#      automated grader relies on.
#   3. No analysis output directory or files are present yet.
#
# The tests purposefully fail with clear, actionable messages when the
# initial state deviates from what the challenge prescribes.
#
# Only stdlib and pytest are used, per instructions.

import os
import textwrap
import configparser
import pytest

CONFIG_DIR = "/home/user/data/configs"
EXPECTED_FILES = {
    "app1.ini",
    "app2.ini",
    "app3.ini",
}
ANALYSIS_DIR = "/home/user/analysis"
AUDIT_LOG = os.path.join(ANALYSIS_DIR, "threshold_audit.log")
STATS_CSV = os.path.join(ANALYSIS_DIR, "threshold_stats.csv")

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def read_ini(path):
    """Return a ConfigParser with *preserved* key order."""
    parser = configparser.ConfigParser()
    # Preserve case & order
    parser.optionxform = str  # type: ignore
    with open(path, "r", encoding="utf-8") as fh:
        parser.read_file(fh)
    return parser


# Expected [thresholds] data for each file
EXPECTED_THRESHOLDS = {
    "app1.ini": {
        "cpu": "85",
        "memory": "65",
        "disk": "90",
    },
    "app2.ini": {
        "cpu": "50",
        "memory": "75",
        "disk": "60",
    },
    "app3.ini": {
        "cpu": "95",
        "memory": "80",
        "disk": "70",
        "temperature": "88",
    },
}

# Raw text of each file (with trailing newline)
RAW_EXPECTED = {
    "app1.ini": textwrap.dedent(
        """\
        [general]
        name = Alpha
        version = 1.2.0

        [network]
        port = 8080
        host = 127.0.0.1

        [thresholds]
        cpu = 85
        memory = 65
        disk = 90
        """
    )
    + "\n",
    "app2.ini": textwrap.dedent(
        """\
        [general]
        name = Beta
        version = 2.4.1

        [network]
        port = 9090
        host = 192.168.1.10

        [thresholds]
        cpu = 50
        memory = 75
        disk = 60
        """
    )
    + "\n",
    "app3.ini": textwrap.dedent(
        """\
        [general]
        name = Gamma
        version = 3.1.5

        [network]
        port = 7070
        host = 10.0.0.5

        [thresholds]
        cpu = 95
        memory = 80
        disk = 70
        temperature = 88
        """
    )
    + "\n",
}

# ---------------------------------------------------------------------------
# Tests for initial environment
# ---------------------------------------------------------------------------


def test_configs_directory_exists(tmp_path_factory):
    assert os.path.isdir(CONFIG_DIR), (
        f"Expected config directory '{CONFIG_DIR}' to exist, "
        "but it is missing."
    )


def test_configs_directory_contains_only_expected_files():
    present = set(os.listdir(CONFIG_DIR))
    missing = EXPECTED_FILES - present
    extra = present - EXPECTED_FILES
    assert not missing, (
        "The following expected INI files are missing from "
        f"'{CONFIG_DIR}': {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected files found in '{CONFIG_DIR}': "
        f"{', '.join(sorted(extra))}. "
        "Only app1.ini, app2.ini and app3.ini should be present."
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_ini_file_content_matches_spec(filename):
    path = os.path.join(CONFIG_DIR, filename)
    assert os.path.isfile(path), f"INI file '{path}' is missing."

    # Compare raw text (robust to newline conventions except final newline)
    with open(path, "r", encoding="utf-8") as fh:
        actual = fh.read()
    expected = RAW_EXPECTED[filename]
    assert actual == expected, (
        f"Contents of '{path}' do not match the expected specification. "
        "Ensure the file is unmodified."
    )

    # Parse and validate [thresholds] keys and values
    parser = read_ini(path)
    assert parser.has_section(
        "thresholds"
    ), f"INI file '{filename}' lacks required [thresholds] section."

    expected_kv = EXPECTED_THRESHOLDS[filename]
    actual_kv = dict(parser.items("thresholds"))

    assert actual_kv == expected_kv, (
        f"[thresholds] section in '{filename}' differs from specification.\n"
        f"Expected: {expected_kv}\nActual:   {actual_kv}"
    )


def test_analysis_directory_does_not_exist_yet():
    # The student shouldn't have created any outputs at this stage.
    assert not os.path.exists(
        ANALYSIS_DIR
    ), f"Directory '{ANALYSIS_DIR}' should not exist before the task is attempted."


def test_output_files_do_not_exist_yet():
    for path in (AUDIT_LOG, STATS_CSV):
        assert not os.path.exists(
            path
        ), f"Output file '{path}' should not pre-exist before the task is attempted."