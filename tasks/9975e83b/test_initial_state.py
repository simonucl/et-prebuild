# test_initial_state.py
"""
Initial-state verification for the HISTTIMEFORMAT compliance task.

This test suite makes sure that the workspace starts from a **clean**
state, i.e. before the student has run any command.  We only inspect
pre-existing resources and *never* look for the files that the student
is supposed to create later (e.g. /home/user/compliance_report.txt).

If a test here fails, it means the template VM / container is already in
a “finished” or otherwise invalid state and the exercise would not make
sense.
"""
import pathlib

import pytest

HOME = pathlib.Path("/home/user")
BASHRC = HOME / ".bashrc"

TARGET_DIRECTIVE = 'export HISTTIMEFORMAT="%F %T "'  # note the trailing space


def _last_non_empty_line(text: str) -> str | None:
    """
    Return the last non-empty line of *text* (strip only the newline
    character, keep leading/trailing spaces), or None if there is none.
    """
    for line in reversed(text.splitlines()):
        if line.strip():          # anything other than whitespace
            return line.rstrip("\n")
    return None


@pytest.mark.dependency(name="bashrc_exists")
def test_bashrc_exists_and_is_regular_file():
    """
    Ensure that /home/user/.bashrc exists and is a regular file.  The
    exercise relies on this file being present so the student can append
    the required directive.
    """
    assert BASHRC.exists(), (
        f"Precondition failure: expected '{BASHRC}' to exist, "
        "but it does not."
    )
    assert BASHRC.is_file(), (
        f"Precondition failure: '{BASHRC}' exists but is not a regular "
        "file (maybe a directory or symlink). It must be a plain file."
    )


@pytest.mark.dependency(depends=["bashrc_exists"])
def test_final_line_not_already_target_directive():
    """
    The *last* non-empty line of ~/.bashrc must *not* already be the
    target directive.  Otherwise the student would start in an already
    compliant state and the exercise would be moot.
    """
    content = BASHRC.read_text(encoding="utf-8", errors="ignore")
    last_line = _last_non_empty_line(content)

    # last_line may be None (empty file) or any other content, but not the directive
    assert last_line != TARGET_DIRECTIVE, (
        f"Precondition failure: the last non-empty line of '{BASHRC}' "
        "is already:\n"
        f'    {TARGET_DIRECTIVE!r}\n'
        "The exercise expects this directive to be missing so that the "
        "student can add it."
    )