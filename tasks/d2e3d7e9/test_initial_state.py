# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state before the
# learner begins the task described in the prompt.  It checks only the
# prerequisite resources that must already be present.  It purposefully
# avoids looking for (or asserting the absence of) any files that will be
# produced as part of the solution workflow.

from pathlib import Path
import configparser
import pytest


INI_PATH = Path("/home/user/db_config.ini")


def _load_ini(path: Path) -> configparser.ConfigParser:
    """
    Load an INI file using the standard library's configparser while
    preserving case‐insensitive keys and stripping surrounding whitespace.
    """
    if not path.exists():
        pytest.fail(
            f"Required INI file not found at {path}. "
            "Ensure the file exists before you begin the task."
        )

    cp = configparser.ConfigParser()
    # ConfigParser normally lower-cases keys and strips whitespace in values;
    # that behavior is acceptable for these assertions.
    try:
        cp.read(path, encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Failed to parse INI file at {path}: {exc}")

    return cp


def test_ini_file_exists_and_has_expected_sections():
    """
    Verify that /home/user/db_config.ini exists and contains the expected
    sections needed for the exercise.
    """
    cp = _load_ini(INI_PATH)

    expected_sections = {"general", "optimizer", "logging"}
    missing = expected_sections.difference(cp.sections())
    assert not missing, (
        "The INI file is missing required section(s): "
        + ", ".join(sorted(missing))
    )


@pytest.mark.parametrize(
    ("option", "expected_value"),
    [
        ("enable_hashjoin", "off"),
        ("enable_mergejoin", "on"),
        ("enable_indexscan", "off"),
    ],
)
def test_optimizer_section_initial_values(option, expected_value):
    """
    Ensure the [optimizer] section starts with the exact values stated in the
    assignment prompt.  This guarantees the learner is starting from the
    correct baseline.
    """
    cp = _load_ini(INI_PATH)

    section = "optimizer"
    assert cp.has_option(section, option), (
        f"The option '{option}' is missing from the [{section}] section "
        f"in {INI_PATH}."
    )

    actual = cp.get(section, option).strip().lower()
    assert actual == expected_value, (
        f"Unexpected initial value for '{option}' in [{section}]. "
        f"Expected '{expected_value}', found '{actual}'."
    )