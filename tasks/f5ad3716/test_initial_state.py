# test_initial_state.py
#
# Pytest suite that verifies the filesystem *before* the student runs
# their data-pipeline.  It checks that the three input files are present
# and unmodified, and that none of the required output artefacts have
# been created yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data" / "users"
OUTPUT_DIR = HOME / "output"

ALPHA_TXT = DATA_DIR / "alpha.txt"
BETA_TXT = DATA_DIR / "beta.txt"
GAMMA_TXT = DATA_DIR / "gamma.txt"

EXPECTED_ALPHA_LINES = [
    "alice,alice@example.com,1001,true",
    "bob,bob@example,1002,TRUE",
    "carol,carol@example.com,1003,false",
]

EXPECTED_BETA_LINES = [
    "dave,dave@example.com,1004,true",
    "eve,eve@example.com,,true",
    "frank,frank@example.com,1006,TRUE",
]

EXPECTED_GAMMA_LINES = [
    "grace,grace@example.com,1007,false",
    "heidi,heidi@sample.com,1008,true",
    "invalidlinewithoutcommas",
]

OUTPUT_FILES = [
    OUTPUT_DIR / "active_users.csv",
    OUTPUT_DIR / "pipeline_errors.log",
    OUTPUT_DIR / "summary.json",
]


@pytest.fixture(scope="module")
def data_dir():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing. "
        "The initial dataset must be present before you start."
    )
    return DATA_DIR


def test_exact_three_txt_files(data_dir):
    """Exactly the three expected '*.txt' files must be present—nothing else."""
    txt_files = sorted(p.name for p in data_dir.glob("*.txt"))
    assert txt_files == ["alpha.txt", "beta.txt", "gamma.txt"], (
        f"Expected only alpha.txt, beta.txt and gamma.txt in {data_dir}. "
        f"Found: {txt_files}"
    )


@pytest.mark.parametrize(
    "path,expected_lines",
    [
        (ALPHA_TXT, EXPECTED_ALPHA_LINES),
        (BETA_TXT, EXPECTED_BETA_LINES),
        (GAMMA_TXT, EXPECTED_GAMMA_LINES),
    ],
)
def test_input_file_contents_unchanged(path: Path, expected_lines):
    """Verify that each input file exists and its content is *exactly* as specified."""
    assert path.is_file(), f"Missing required input file: {path}"
    file_lines = path.read_text(encoding="utf-8").splitlines()
    assert file_lines == expected_lines, (
        f"File {path} has been modified or corrupted.\n"
        f"Expected lines:\n{expected_lines}\n\nActual lines:\n{file_lines}"
    )


def test_no_output_files_exist_yet():
    """
    Before the student runs their pipeline, no deliverable files should exist.
    If they do, it means a previous run polluted the workspace.
    """
    for artefact in OUTPUT_FILES:
        assert not artefact.exists(), (
            f"Output artefact {artefact} already exists. "
            "The environment must start clean so the pipeline can create it."
        )