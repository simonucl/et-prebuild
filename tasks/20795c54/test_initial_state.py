# test_initial_state.py
#
# This test-suite validates the **initial** state of the operating
# system / file-system **before** the student performs any action.
#
# It checks only the files that already have to exist and must *not*
# inspect any of the yet-to-be-produced output artefacts.
#
# The tests will fail with clear messages if the expected pre-condition
# is not met.

import os
import stat
import textwrap
import pytest

CONFIG_PATH = "/home/user/appd/config.ini"


@pytest.fixture(scope="module")
def config_text():
    """Return the raw text of the initial config file."""
    if not os.path.isfile(CONFIG_PATH):
        pytest.fail(f"Required config file missing: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


def test_config_ini_exists_and_is_file():
    assert os.path.exists(CONFIG_PATH), (
        f"Expected {CONFIG_PATH} to exist, but it does not."
    )
    assert os.path.isfile(CONFIG_PATH), (
        f"Expected {CONFIG_PATH} to be a regular file."
    )

    # World-readable (0644 is fine); owner/group bits may vary.
    st = os.stat(CONFIG_PATH)
    mode = stat.S_IMODE(st.st_mode)
    assert mode & stat.S_IROTH, (
        f"{CONFIG_PATH} must be world-readable (at least mode 0o644). "
        f"Current mode is {oct(mode)}."
    )


def test_first_line_is_not_hardened_comment_yet(config_text):
    # The hardening step has *not* happened yet, so the file must NOT
    # start with the comment line.
    first_line = config_text.splitlines()[0]
    assert first_line.strip() != "# Hardened by SecOps", (
        "The file already contains the hardening comment as first line, "
        "but this should be added *after* the task is completed."
    )


def test_initial_content_matches_expected(config_text):
    # The exact initial content that must be present *before*
    # the student touches the file.
    expected_content = textwrap.dedent(
        """\
        [core]
        enabled=true
        secure=true
        timeout=30

        [analytics]
        enabled=true
        secure=false
        sample_rate=10

        [network]
        enabled=true
        secure=true
        port=8080

        [logging]
        enabled=true
        secure=false
        level=debug

        [beta]
        enabled=true
        secure=false
        experimental=true
        """
    )
    # We normalise trailing newlines to avoid platform vagaries.
    assert config_text.strip() == expected_content.strip(), (
        "The initial contents of /home/user/appd/config.ini do not match "
        "the expected baseline. Make sure the starting file is exactly "
        "as provided in the exercise description, without the hardening "
        "comment or any [compliance] section."
    )


def test_no_compliance_section_yet(config_text):
    assert "[compliance]" not in config_text, (
        "The [compliance] section is already present, but it must be added "
        "only after the hardening steps."
    )