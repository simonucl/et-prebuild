# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system /
# file-system before the student starts working on the assignment.
#
# IMPORTANT:
#   • We intentionally do **NOT** check for any paths that the student is
#     supposed to create later (e.g. “/home/user/remote_server/docs_remote/”
#     or anything inside “/home/user/sync_logs/”).
#   • Only the pre-existing structure under “/home/user/docs_local/” and the
#     mere existence of “/home/user/remote_server/” are verified.
#
# The tests must pass unchanged in the pristine environment provided by the
# course infrastructure.  Any failure means the sandbox is not in the expected
# initial state.

import os
from pathlib import Path

DOCS_LOCAL = Path("/home/user/docs_local")
REMOTE_SERVER = Path("/home/user/remote_server")


def test_docs_local_structure_and_contents():
    """Validate the layout and contents of /home/user/docs_local/."""
    assert DOCS_LOCAL.is_dir(), (
        "Directory '/home/user/docs_local/' is missing – it must be present "
        "before starting the task."
    )

    # 1. index.md
    index_md = DOCS_LOCAL / "index.md"
    assert index_md.is_file(), "Expected file 'index.md' is missing."
    assert index_md.read_text(encoding="utf-8") == "Hello, world.\n", (
        "Unexpected content in 'index.md'."
    )

    # 2. .gitignore
    gitignore = DOCS_LOCAL / ".gitignore"
    assert gitignore.is_file(), "Expected file '.gitignore' is missing."
    git_content_first_line = gitignore.read_text(encoding="utf-8").splitlines()[0]
    assert git_content_first_line == "*.tmp", (
        "First line of '.gitignore' should be '*.tmp'."
    )

    # 3. README.md -> index.md (symlink)
    readme = DOCS_LOCAL / "README.md"
    assert readme.is_symlink(), "README.md must be a symbolic link."
    assert os.readlink(readme) == "index.md", (
        "README.md should link to 'index.md' (relative symbolic link)."
    )

    # 4. images/diagram.png (0-byte placeholder)
    images_dir = DOCS_LOCAL / "images"
    assert images_dir.is_dir(), "Sub-directory 'images/' is missing."
    diagram_png = images_dir / "diagram.png"
    assert diagram_png.is_file(), "Expected file 'images/diagram.png' is missing."
    assert diagram_png.stat().st_size == 0, (
        "'diagram.png' is expected to be an empty (0-byte) placeholder file."
    )

    # 5. intro/overview.md
    intro_dir = DOCS_LOCAL / "intro"
    assert intro_dir.is_dir(), "Sub-directory 'intro/' is missing."
    overview_md = intro_dir / "overview.md"
    assert overview_md.is_file(), "Expected file 'intro/overview.md' is missing."
    assert overview_md.read_text(encoding="utf-8") == "Project overview.\n", (
        "Unexpected content in 'intro/overview.md'."
    )


def test_remote_server_directory_exists():
    """
    The top-level remote server directory must exist at the outset.
    We purposely do NOT check for 'docs_remote/' because it will be created
    by the student during the sync operation.
    """
    assert REMOTE_SERVER.is_dir(), (
        "Directory '/home/user/remote_server/' is missing – the base directory "
        "for the simulated remote server must pre-exist."
    )