# test_initial_state.py
"""
Pytest suite that verifies the *initial* state of the operating system / filesystem
before the student starts working on the “performance-engineering” task.

What we assert:

1. The three raw profiling log files exist **exactly** at the required absolute paths.
2. Each raw file holds the expected lines (ignoring the amount of inner whitespace).
3. No processed artefacts or their parent directories are present yet.

If any assertion fails, the error message tells the student precisely what is wrong.
"""

from pathlib import Path
import pytest
import stat

HOME = Path("/home/user")
RAW_DIR = HOME / "perf" / "raw"
PROCESSED_DIR = HOME / "perf" / "processed"
REPORTS_DIR = HOME / "perf" / "reports"

RAW_FILES_EXPECTED = {
    RAW_DIR / "app1.log": [
        "[2023-02-10 15:12:01] FUNC=initSystem   CPU_MS=5  MEM_MB=30",
        "[2023-02-10 15:12:05] FUNC=loadConfig   CPU_MS=8  MEM_MB=45",
        "[2023-02-10 15:12:10] FUNC=parseData    CPU_MS=25 MEM_MB=550",
        "[2023-02-10 15:12:12] FUNC=renderFrame  CPU_MS=40 MEM_MB=300",
    ],
    RAW_DIR / "app2.log": [
        "[2023-02-10 15:12:02] FUNC=connectDB    CPU_MS=30 MEM_MB=400",
        "[2023-02-10 15:12:08] FUNC=queryDB      CPU_MS=80 MEM_MB=650",
        "[2023-02-10 15:12:13] FUNC=closeDB      CPU_MS=10 MEM_MB=120",
    ],
    RAW_DIR / "app3.log": [
        "[2023-02-10 15:12:03] FUNC=authUser     CPU_MS=60 MEM_MB=200",
        "[2023-02-10 15:12:07] FUNC=updateCache  CPU_MS=15 MEM_MB=100",
        "[2023-02-10 15:12:09] FUNC=compressData CPU_MS=50 MEM_MB=700",
        "[2023-02-10 15:12:11] FUNC=encryptData  CPU_MS=35 MEM_MB=480",
    ],
}

OUTPUT_FILES = [
    PROCESSED_DIR / "master.log",
    PROCESSED_DIR / "top_cpu.txt",
    PROCESSED_DIR / "high_mem.log",
    REPORTS_DIR / "summary_report.md",
]


def _normalize(line: str) -> str:
    """
    Collapse all internal whitespace to single spaces so that files which
    use tabs or double-spaces still match the expected canonical form.
    """
    return " ".join(line.strip().split())


@pytest.mark.parametrize("file_path", RAW_FILES_EXPECTED.keys())
def test_raw_log_files_exist(file_path: Path):
    assert file_path.exists(), (
        f"Required raw file {file_path} is missing.\n"
        "Make sure the unprocessed logs are placed exactly as specified."
    )
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    # Permissions: must be at least readable by owner (and usually by everyone)
    mode = file_path.stat().st_mode
    assert bool(mode & stat.S_IRUSR), f"{file_path} is not readable (missing read bit)."


@pytest.mark.parametrize("file_path, expected_lines", RAW_FILES_EXPECTED.items())
def test_raw_log_file_contents(file_path: Path, expected_lines):
    with file_path.open("r", encoding="utf-8") as fh:
        actual_lines = [_normalize(l) for l in fh.readlines()]

    expected_norm = [_normalize(l) for l in expected_lines]

    # Line count must match exactly.
    assert len(actual_lines) == len(
        expected_norm
    ), f"{file_path} should contain {len(expected_norm)} lines but has {len(actual_lines)}."

    # Each individual line must match after normalisation.
    for idx, (act, exp) in enumerate(zip(actual_lines, expected_norm), start=1):
        assert act == exp, (
            f"Mismatch in {file_path} on line {idx}.\n"
            f"Expected: {exp!r}\n"
            f"Found   : {act!r}\n"
            "Ensure the raw logs remain unaltered."
        )


def test_no_processed_directories_or_files_exist_yet():
    """
    Before the student runs their solution, *no* processed artefacts should exist.
    """
    assert not PROCESSED_DIR.exists(), (
        f"Directory {PROCESSED_DIR} already exists. "
        "Processed artefacts must not be present before the task is executed."
    )
    assert not REPORTS_DIR.exists(), (
        f"Directory {REPORTS_DIR} already exists. "
        "Reports must not be present before the task is executed."
    )

    # For extra safety, in case the directories exist but are empty, also check files
    for path in OUTPUT_FILES:
        assert not path.exists(), (
            f"Output file {path} already exists. "
            "The workspace should start in a clean state."
        )