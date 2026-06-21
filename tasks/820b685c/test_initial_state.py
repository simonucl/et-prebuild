# test_initial_state.py
#
# Pytest suite to validate the operating-system state *before* the student
# performs any action for the “INI summary” exercise.
#
# This file checks only the pre-existing artefacts that the student is told
# to rely on.  Per the specification, it purposefully does NOT test for the
# presence (or absence) of any of the output files or directories that the
# student will create.

import os
import stat
import configparser
import pytest

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

INI_PATH = "/home/user/project/perf_settings.ini"

EXPECTED_CONTENT = {
    "database": {
        "max_connections": "200",
        "timeout_seconds": "60",
    },
    "server": {
        "thread_pool_size": "32",
        "enable_caching": "true",
    },
    "logging": {
        "level": "INFO",
        "rotate": "daily",
    },
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def _world_readable(path: str) -> bool:
    """Return True if the file is world-readable (others have the read bit)."""
    mode = os.stat(path).st_mode
    return bool(mode & stat.S_IROTH)


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------


def test_ini_file_exists_and_is_world_readable():
    """
    The initial fixture must provide `/home/user/project/perf_settings.ini`
    as a regular, UTF-8 text file that is world-readable.
    """
    assert os.path.isfile(
        INI_PATH
    ), f"Expected INI file at {INI_PATH!r} but it is missing or not a regular file."

    assert _world_readable(
        INI_PATH
    ), f"{INI_PATH!r} exists but is not world-readable (others lack read permission)."

    # Attempt to open with UTF-8 to guarantee it's valid text.
    try:
        with open(INI_PATH, "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError as exc:
        pytest.fail(f"{INI_PATH!r} is not valid UTF-8 text: {exc}")


def test_ini_file_contains_expected_sections_and_keys():
    """
    Validate that the INI file contains every required section and key/value
    exactly as the exercise description specifies.
    """
    parser = configparser.ConfigParser()
    # Preserve case for the value comparison; ConfigParser lower-cases
    # option names by default, which matches the expected keys.
    parser.read(INI_PATH, encoding="utf-8")

    # 1. Correct number of sections
    found_sections = parser.sections()
    assert len(found_sections) == len(
        EXPECTED_CONTENT
    ), (
        "Unexpected number of top-level sections in the INI file.\n"
        f"Expected: {len(EXPECTED_CONTENT)}, Found: {len(found_sections)}\n"
        f"Sections present: {found_sections}"
    )

    # 2. Each expected section and its keys/values.
    for section, expected_kvs in EXPECTED_CONTENT.items():
        assert parser.has_section(
            section
        ), f"The INI file is missing the [{section}] section."

        for key, expected_val in expected_kvs.items():
            assert parser.has_option(
                section, key
            ), f"Missing key {key!r} in section [{section}]."

            actual_val = parser.get(section, key, raw=True).strip()
            assert (
                actual_val == expected_val
            ), (
                f"Value mismatch for {key!r} in section [{section}].\n"
                f"Expected: {expected_val!r}\n"
                f"Found:    {actual_val!r}"
            )