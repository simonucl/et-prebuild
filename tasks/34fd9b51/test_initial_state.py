# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student carries out any task-related actions.

import os
import stat
import pytest

HOME = "/home/user"
DATASET_DIR = os.path.join(HOME, "datasets", "sentiment140")

# Absolute paths to the three required input files
INPUT_FILES = {
    os.path.join(DATASET_DIR, "train_part1.txt"): (
        "I love this movie\tpositive\n"
        "It was great!\tpositive\n"
    ),
    os.path.join(DATASET_DIR, "train_part2.txt"): (
        "I hate this movie\tnegative\n"
        "It was terrible!\tnegative\n"
    ),
    os.path.join(DATASET_DIR, "train_part3.txt"): (
        "It was okay\tneutral\n"
        "Not bad, not good\tneutral\n"
    ),
}

# Paths that must *not* exist yet (they will be created by the student later)
FORBIDDEN_OUTPUTS = [
    os.path.join(DATASET_DIR, "sentiment140_parts.tar.gz"),
    os.path.join(DATASET_DIR, "checksums.sha256"),
    os.path.join(DATASET_DIR, "verification.log"),
]


def _mode_is_rw_by_user(mode: int) -> bool:
    """
    Return True iff the st_mode bits correspond to -rw-r--r-- or similar, i.e.
    user read+write and *at least* user read is present.
    """
    return bool(mode & stat.S_IRUSR) and bool(mode & stat.S_IWUSR)


@pytest.fixture(scope="session")
def dataset_dir_exists():
    assert os.path.isdir(DATASET_DIR), (
        f"Expected directory {DATASET_DIR} to exist."
    )
    # Check writability
    assert os.access(DATASET_DIR, os.W_OK), (
        f"Directory {DATASET_DIR} is not writable by the current user."
    )
    return True


@pytest.mark.usefixtures("dataset_dir_exists")
class TestInitialDatasetState:
    """Validates the pristine state of the sentiment140 dataset directory."""

    @pytest.mark.parametrize("abs_path,expected_content", INPUT_FILES.items())
    def test_file_exists_with_correct_content_and_permissions(
        self, abs_path, expected_content
    ):
        # 1. Existence
        assert os.path.isfile(
            abs_path
        ), f"Required file {abs_path} does not exist."

        # 2. Permissions: readable & writable by user
        st = os.stat(abs_path)
        assert _mode_is_rw_by_user(
            st.st_mode
        ), f"File {abs_path} is not readable/writable (0644) by the user."

        # 3. Content exactly matches ground truth (byte-for-byte)
        with open(abs_path, "r", encoding="utf-8") as fh:
            actual = fh.read()
        assert (
            actual == expected_content
        ), f"Content of {abs_path} does not match the expected ground truth."

    @pytest.mark.parametrize("output_path", FORBIDDEN_OUTPUTS)
    def test_no_task_outputs_exist_yet(self, output_path):
        assert not os.path.exists(
            output_path
        ), (
            f"File {output_path} should NOT exist prior to running the "
            "packaging task."
        )