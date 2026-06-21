# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state
# is correct **before** the student begins working on the task.
#
# Checked items:
#   • The raw-log directory exists.
#   • The two expected CSV files are present and are regular files.
#   • Each file’s textual content matches the canonical truth exactly,
#     including the order of lines and the presence of a trailing newline.
#
# IMPORTANT:  Per specification, this test suite intentionally
# does *not* touch or mention any output directories / files.

from pathlib import Path
import pytest

RAW_DIR = Path("/home/user/restore_tests/raw_logs")

EXPECTED_LOGS = {
    "log_day1.csv": [
        "2023-09-01T02:13:22Z,/etc/nginx/nginx.conf,RESTORED",
        "2023-09-01T02:14:01Z,/var/www/html/index.html,RESTORED",
        "2023-09-01T02:14:45Z,/etc/nginx/nginx.conf,RESTORED",
        "2023-09-01T02:15:10Z,/var/www/html/index.html,FAILURE",
        "2023-09-01T02:15:55Z,/home/user/.bashrc,RESTORED",
        "2023-09-01T02:16:27Z,/etc/nginx/nginx.conf,RESTORED",
        "2023-09-01T02:17:08Z,/var/www/html/main.css,RESTORED",
    ],
    "log_day2.csv": [
        "2023-09-02T11:05:00Z,/etc/nginx/nginx.conf,RESTORED",
        "2023-09-02T11:06:14Z,/var/www/html/index.html,RESTORED",
        "2023-09-02T11:06:52Z,/home/user/.bashrc,RESTORED",
        "2023-09-02T11:07:33Z,/var/www/html/main.css,RESTORED",
        "2023-09-02T11:08:17Z,/etc/nginx/nginx.conf,RESTORED",
        "2023-09-02T11:08:59Z,/home/user/.bashrc,FAILURE",
        "2023-09-02T11:09:41Z,/var/www/html/index.html,RESTORED",
    ],
}

def _read_file_text(path: Path) -> str:
    """Return file content as UTF-8 text or provide a clear pytest failure."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file not found: {path}")
    except OSError as exc:
        pytest.fail(f"Could not read {path}: {exc}")

def test_raw_log_directory_exists():
    assert RAW_DIR.exists(), f"Directory missing: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"Expected a directory at {RAW_DIR}, but found something else."

@pytest.mark.parametrize("filename,expected_lines", EXPECTED_LOGS.items())
def test_log_files_exist_and_match_truth(filename, expected_lines):
    file_path = RAW_DIR / filename

    # --- Existence & type checks -------------------------------------------------
    assert file_path.exists(), f"Required log file is missing: {file_path}"
    assert file_path.is_file(), f"Expected {file_path} to be a regular file."

    # --- Content checks ----------------------------------------------------------
    content = _read_file_text(file_path)

    # Ensure there is a single trailing newline character
    assert content.endswith("\n"), (
        f"{file_path} must end with a single newline character (\\n)."
    )

    # Split lines (splitlines() discards the newline characters)
    lines = content.splitlines()
    assert lines == expected_lines, (
        f"Content mismatch in {file_path}.\n"
        f"Expected:\n{expected_lines}\n\nFound:\n{lines}"
    )

    # Sanity-check CSV structure: exactly three comma-separated fields per line
    for idx, line in enumerate(lines, start=1):
        parts = line.split(",")
        assert len(parts) == 3, (
            f"Line {idx} in {file_path} does not have exactly three comma-separated "
            f"fields: {line!r}"
        )
        # Second field must be an absolute path (start with '/')
        path_field = parts[1]
        assert path_field.startswith("/"), (
            f"Line {idx} in {file_path} has a non-absolute path: {path_field!r}"
        )