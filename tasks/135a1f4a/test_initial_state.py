# test_initial_state.py
#
# This test-suite validates *the starting state* of the workspace **before**
# the student makes any changes.  It asserts that both configuration files
# exist with their original, unmodified contents so that follow-up tests
# can safely confirm the student’s edits.
#
# IMPORTANT
# ---------
# * DO NOT touch any output artefacts that will be produced by the student
#   (e.g. /home/user/debug_logs/verification.log).  We deliberately avoid
#   referencing them here.
# * Only stdlib + pytest are used.
# * All assertion error messages are written so that a failure clearly
#   indicates what is missing or unexpectedly changed.

import pathlib
import sys
import textwrap

import pytest

HOME = pathlib.Path("/home/user")
CFG_DIR = HOME / "app_config"
CFG_YAML = CFG_DIR / "config.yaml"
TOML_FILE = CFG_DIR / "logging.toml"


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def read_text(path: pathlib.Path) -> str:
    """Return text from *path*, raising an assertion error if the file
    does not exist or is unreadable."""
    assert path.exists(), f"Expected file {path} to exist."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        raise AssertionError(f"Unable to read {path}: {exc}") from exc


def parse_toml(path: pathlib.Path) -> dict:
    """
    Parse a TOML file using the stdlib's tomllib (3.11+) and return a dict.
    If tomllib is unavailable (Python < 3.11), the test is skipped.
    """
    try:
        import tomllib  # Python ≥3.11
    except ModuleNotFoundError:
        pytest.skip("Python < 3.11 detected; tomllib unavailable to parse TOML.")
    with path.open("rb") as fp:
        return tomllib.load(fp)


# --------------------------------------------------------------------------- #
# Tests for /home/user/app_config/config.yaml                                 #
# --------------------------------------------------------------------------- #
def test_config_yaml_exists():
    assert CFG_YAML.is_file(), f"Expected YAML file at {CFG_YAML}."


def test_config_yaml_has_original_logging_level():
    """
    The YAML must *still* have logging.level == \"INFO\" before the student
    changes it to DEBUG.  Also ensure DEBUG is not already present.
    """
    content = read_text(CFG_YAML)

    # Strip common leading indent so we can compare blocks easily.
    expected_block = textwrap.dedent(
        """
        logging:
          level: "INFO"
          format: "json"
        """
    ).strip()

    assert (
        expected_block in content
    ), "Initial logging block not found or already modified in config.yaml."

    assert '"DEBUG"' not in content, (
        "config.yaml already contains DEBUG; it should still be INFO at the "
        "start of the exercise."
    )


# --------------------------------------------------------------------------- #
# Tests for /home/user/app_config/logging.toml                                #
# --------------------------------------------------------------------------- #
def test_logging_toml_exists():
    assert TOML_FILE.is_file(), f"Expected TOML file at {TOML_FILE}."


@pytest.mark.skipif(sys.version_info < (3, 11), reason="tomllib requires Python 3.11+")
def test_logging_toml_has_original_values():
    """
    Validate that logging.toml is still in its initial state.
    """
    data = parse_toml(TOML_FILE)

    # -------- [output.console] table --------
    console = data.get("output", {}).get("console")
    assert console is not None, "[output.console] table missing from logging.toml."
    assert console.get("enabled") is True, "output.console.enabled should be true."
    assert (
        console.get("level") == "INFO"
    ), "output.console.level should be 'INFO' initially."

    # -------- [output.file] table --------
    file_tbl = data.get("output", {}).get("file")
    assert file_tbl is not None, "[output.file] table missing from logging.toml."

    assert file_tbl.get("enabled") is False, "output.file.enabled should be false."
    assert (
        file_tbl.get("path") == "/var/log/app/service.log"
    ), "output.file.path should be the original path."
    assert (
        file_tbl.get("level") == "INFO"
    ), "output.file.level should be 'INFO' initially."
    assert (
        file_tbl.get("rotation") == "daily"
    ), "output.file.rotation should be 'daily' initially."

    # -------- [filters] table should NOT exist yet --------
    assert "filters" not in data, "[filters] table should NOT exist before the task."