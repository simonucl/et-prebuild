# test_initial_state.py
#
# This pytest suite validates the machine **before** any backup-automation
# steps are carried out.  It intentionally limits its checks to the parts of
# the system that should already exist.  Output artefacts and directories
# that the learner is expected to create later are *not* examined here.

import pathlib

HOME = pathlib.Path("/home/user")
BASHRC = HOME / ".bashrc"
SOURCE_LINE = "source /home/user/.db_backup.env"


def test_home_directory_exists():
    """
    The generic home directory must already be present; otherwise nothing
    else can be configured.
    """
    assert HOME.is_dir(), f"Expected the home directory {HOME} to exist."


def test_bashrc_exists():
    """
    The default ~/.bashrc file should ship with the base image.
    """
    assert BASHRC.is_file(), (
        "Expected the default Bash initialisation file "
        f"{BASHRC} to exist before any modifications."
    )


def test_bashrc_does_not_already_source_env_file():
    """
    The `.db_backup.env` file is part of the *future* configuration.  Its
    sourcing line must not be present yet.
    """
    bashrc_contents = BASHRC.read_text().splitlines()
    offending_lines = [
        line for line in bashrc_contents if line.strip() == SOURCE_LINE
    ]
    assert (
        len(offending_lines) == 0
    ), (
        f"The line '{SOURCE_LINE}' should NOT be present in {BASHRC} "
        "prior to the backup-automation task."
    )