# test_initial_state.py
#
# This pytest-suite validates the **initial** filesystem/OS state for the
# “Python-file catalogue” exercise _before_ the student performs any action.
# It intentionally does **not** look for the expected output artefacts
# (SQLite DB, JSON export, log file) – only the inputs that must already be
# present.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SRC_ROOT = HOME / "projects" / "webapp" / "src"


@pytest.fixture(scope="module")
def expected_files():
    """
    Return a mapping of every *.py file that must exist _before_ the student
    starts working.  The mapping contains the absolute Path, the exact file
    contents (including the terminating newline), the expected SHA-256 digest,
    and the expected file size in bytes.
    """
    files = {
        SRC_ROOT / "app.py": "print('Hello World')\n",
        SRC_ROOT / "config.py": "DEBUG = True\n",
        SRC_ROOT / "utils" / "helpers.py": "def add(a, b):\n    return a + b\n",
    }

    # Build enriched dict: {path: {'content': str, 'sha256': str, 'size': int}}
    enriched = {}
    for path, content in files.items():
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        enriched[path] = {
            "content": content,
            "sha256": digest,
            "size": len(content.encode("utf-8")),
        }
    return enriched


def test_src_root_exists():
    """The base source directory must be present and be a directory."""
    assert SRC_ROOT.exists(), (
        f"Required directory {SRC_ROOT} does not exist. "
        "The exercise expects the web-application source tree to be present."
    )
    assert SRC_ROOT.is_dir(), f"{SRC_ROOT} exists but is not a directory."


def test_expected_python_files_exist(expected_files):
    """
    Verify that every required *.py file exists with the exact content,
    size and SHA-256 digest specified in the task description.
    """
    for path, meta in expected_files.items():
        assert path.exists(), (
            f"Expected file {path} is missing.\n"
            "Ensure the developer’s original source tree is intact."
        )
        assert path.is_file(), f"{path} exists but is not a regular file."

        actual_bytes = path.read_bytes()

        # Size check
        assert len(actual_bytes) == meta["size"], (
            f"File {path} has size {len(actual_bytes)} bytes, "
            f"expected {meta['size']} bytes."
        )

        # Content check (exact match)
        assert actual_bytes.decode("utf-8") == meta["content"], (
            f"File {path} does not match the expected content."
        )

        # SHA-256 check
        actual_sha = hashlib.sha256(actual_bytes).hexdigest()
        assert actual_sha == meta["sha256"], (
            f"File {path} has SHA-256 digest {actual_sha}, "
            f"expected {meta['sha256']}."
        )


def test_no_extra_python_files(expected_files):
    """
    The spec says there are *exactly* three Python files under
    /home/user/projects/webapp/src and its subdirectories.  Make sure no extra
    .py files are present.
    """
    discovered = [
        Path(root) / fname
        for root, _dirs, files in os.walk(SRC_ROOT)
        for fname in files
        if fname.endswith(".py")
    ]

    expected_set = set(expected_files.keys())
    discovered_set = set(discovered)

    # Helpful diffs
    missing = expected_set - discovered_set
    unexpected = discovered_set - expected_set

    assert not missing, (
        "The following required *.py files are missing under the source tree:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )

    assert not unexpected, (
        "Unexpected Python files were found under the source tree. "
        "The exercise should start with exactly three *.py files:\n"
        + "\n".join(str(p) for p in sorted(unexpected))
    )