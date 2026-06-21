# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem state **before**
# the student runs any commands.  It purposefully avoids checking for
# the final artefact (/home/user/webapp/logs/js_checksums.log) because
# that file must be created by the student later on.

import hashlib
from pathlib import Path

BASE_DIR = Path("/home/user/webapp").resolve()

# Mapping: absolute file path  ->  expected file content (including trailing \n)
EXPECTED_FILES = {
    BASE_DIR / "assets/js/script1.js":
        "console.log('Script One');\n",
    BASE_DIR / "assets/js/script2.js":
        "console.log('Script Two');\n",
    BASE_DIR / "src/app.js":
        "console.log('Main App');\n",
    BASE_DIR / "src/utils/helper.js":
        "export function greet() { return 'Hello'; }\n",
    BASE_DIR / "README.md":
        "# Sample project\n",
}

# Directories that must already exist (full, absolute paths)
EXPECTED_DIRECTORIES = [
    BASE_DIR,
    BASE_DIR / "assets",
    BASE_DIR / "assets/js",
    BASE_DIR / "src",
    BASE_DIR / "src/utils",
]


def _md5(s: str) -> str:
    """
    Helper: return lower-case hex md5 of given string (assumed UTF-8).
    """
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def test_directories_exist():
    """
    Ensure that all required directories exist **before** the student
    starts working.
    """
    missing = [str(p) for p in EXPECTED_DIRECTORIES if not p.is_dir()]
    assert not missing, (
        "The following required directories are missing:\n  " +
        "\n  ".join(missing)
    )


def test_files_exist_with_correct_contents_and_md5():
    """
    • Every expected file exists.
    • The content of each file exactly matches the specification,
      including trailing new-lines.
    • The on-disk MD5 checksum matches the MD5 of the expected string.
    """
    for path, expected_text in EXPECTED_FILES.items():
        # 1. Presence
        assert path.is_file(), f"Required file is missing: {path}"

        # 2. Content check
        on_disk_bytes = path.read_bytes()
        try:
            on_disk_text = on_disk_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"{path} is not valid UTF-8: {exc}") from exc

        assert on_disk_text == expected_text, (
            f"Content mismatch in {path}.\n"
            f"Expected:\n{expected_text!r}\n"
            f"Found:\n{on_disk_text!r}"
        )

        # 3. MD5 verification
        expected_md5 = _md5(expected_text)
        on_disk_md5 = hashlib.md5(on_disk_bytes).hexdigest()
        assert on_disk_md5 == expected_md5, (
            f"MD5 mismatch for {path}.\n"
            f"Expected: {expected_md5}\n"
            f"Found   : {on_disk_md5}"
        )