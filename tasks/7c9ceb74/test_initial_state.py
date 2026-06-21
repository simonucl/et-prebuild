# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state before the student
# performs any actions on the configuration files.  It confirms that the two
# expected configuration files are present with their original contents and
# that no optimisation log exists yet.

import os
import textwrap

BASE_DIR = "/home/user/db_configs"
YAML_PATH = os.path.join(BASE_DIR, "db_settings.yaml")
TOML_PATH = os.path.join(BASE_DIR, "replication.toml")
LOG_PATH = os.path.join(BASE_DIR, "optimization_log.txt")


def test_db_configs_directory_exists():
    assert os.path.isdir(
        BASE_DIR
    ), f"Expected directory {BASE_DIR!r} to exist, but it is missing."


def test_expected_files_present_and_no_extras():
    """
    The directory should contain *exactly* the two configuration files (no log
    yet, no stray temp files, etc.).
    """
    expected = {"db_settings.yaml", "replication.toml"}
    actual = set(os.listdir(BASE_DIR))
    missing = expected - actual
    extras = actual - expected
    assert not missing, f"Missing expected file(s): {', '.join(sorted(missing))}"
    assert (
        not extras
    ), f"Unexpected extra file(s) present in {BASE_DIR}: {', '.join(sorted(extras))}"


def test_db_settings_yaml_initial_content(tmp_path):
    assert os.path.isfile(
        YAML_PATH
    ), f"File {YAML_PATH!r} is missing; it should exist before editing."

    expected_content = textwrap.dedent(
        """\
        database:
          host: localhost
          port: 5432
          pool:
            size: 10
            timeout: 300

        queries:
          optimizer:
            enable: false
            cost_threshold: 100
        """
    )

    with open(YAML_PATH, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert (
        actual_content == expected_content
    ), (
        "The YAML configuration file does not match the expected *initial* "
        "state.\n\nExpected:\n"
        f"{expected_content!r}\n\nActual:\n{actual_content!r}"
    )


def test_replication_toml_initial_content():
    assert os.path.isfile(
        TOML_PATH
    ), f"File {TOML_PATH!r} is missing; it should exist before editing."

    expected_content = textwrap.dedent(
        """\
        [replication]
        enabled = false
        max_replicas = 2

        [maintenance]
        vacuum = "daily"
        """
    )

    with open(TOML_PATH, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert (
        actual_content == expected_content
    ), (
        "The TOML configuration file does not match the expected *initial* "
        "state.\n\nExpected:\n"
        f"{expected_content!r}\n\nActual:\n{actual_content!r}"
    )


def test_optimization_log_not_present():
    assert not os.path.exists(
        LOG_PATH
    ), f"Audit log {LOG_PATH!r} should *not* exist before the student creates it."