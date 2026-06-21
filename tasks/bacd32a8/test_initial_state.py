# test_initial_state.py
#
# Pytest suite to verify the *initial* state of the filesystem
# BEFORE the student carries out any actions for the “mini stack”
# assignment.  All deliverable artefacts are expected to be ABSENT.
#
# If any of the required files / directories already exist, the
# environment is considered “dirty” and the test suite will fail with
# a clear explanation so that the student (and the autograder) start
# from a known-clean slate.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user").expanduser()

# All paths that MUST NOT exist at the start of the exercise.
ARTEFACT_DIRS = [
    HOME / "iot_edge",
    HOME / "iot_edge" / "bin",
    HOME / "iot_edge" / "config",
    HOME / "iot_edge" / "logs",
    HOME / "iot_edge" / "data",
]

ARTEFACT_FILES = [
    HOME / "iot_edge" / "config" / "mosquitto_edge.conf",
    HOME / "iot_edge" / "bin" / "edge_collector.py",
    HOME / "iot_edge" / "start_edge_stack.sh",
    HOME / "iot_edge" / "deploy.log",
]


@pytest.mark.describe("Prerequisite: The home directory for the non-privileged user must exist.")
def test_home_directory_exists():
    assert HOME.is_dir(), (
        f"The expected home directory {HOME} does not exist.\n"
        "The exercise assumes a non-privileged user whose home is /home/user."
    )


@pytest.mark.describe("Clean slate: None of the target directories should pre-exist.")
@pytest.mark.parametrize("path", ARTEFACT_DIRS)
def test_directories_absent(path: Path):
    assert not path.exists(), (
        f"Unexpected directory found: {path}\n"
        "The working tree must be created by the student; "
        "it should not exist beforehand."
    )


@pytest.mark.describe("Clean slate: None of the target files should pre-exist.")
@pytest.mark.parametrize("path", ARTEFACT_FILES)
def test_files_absent(path: Path):
    assert not path.exists(), (
        f"Unexpected file found: {path}\n"
        "All deliverable files must be created by the student; "
        "they should not exist beforehand."
    )