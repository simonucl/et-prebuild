# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state
for the “deployment-engineer” exercise.

The checks intentionally **fail** if anything has already been created or
started, because the student’s job is to produce those artefacts / processes.
Only the Python standard library and pytest are used.
"""

import os
import stat
import subprocess
from pathlib import Path

DEPLOY_DIR = Path("/home/user/deployment")
DEPLOY_SCRIPT = DEPLOY_DIR / "deploy_app.sh"
PID_FILE = DEPLOY_DIR / "deployment.pid"
SNAPSHOT_FILE = DEPLOY_DIR / "process_snapshot.log"


def _collect_running_deploy_pids():
    """
    Return a list of PIDs for any running instances of deploy_app.sh.

    We fall back on parsing `ps -eo pid,command` to remain in stdlib-only
    territory (pgrep is not guaranteed to be present).
    """
    try:
        ps_out = subprocess.check_output(["ps", "-eo", "pid,args"], text=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        # The platform must provide `ps`; if not, make the test abort early.
        pytest.fail(f"Unable to execute `ps` to inspect running processes: {exc}")

    pids = []
    for line in ps_out.strip().splitlines():
        # Each line: "<PID> <command ...>"
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        pid_str, cmd = parts
        if "/home/user/deployment/deploy_app.sh" in cmd:
            # Guard against the header row (which on some ps variants is "PID COMMAND")
            if pid_str.isdigit():
                pids.append(int(pid_str))
    return pids


def test_deploy_directory_exists_and_writable():
    assert DEPLOY_DIR.is_dir(), (
        f"Expected directory {DEPLOY_DIR} to exist, but it is missing or not a directory."
    )
    assert os.access(DEPLOY_DIR, os.W_OK), (
        f"Directory {DEPLOY_DIR} is not writable by the current user."
    )


def test_deploy_script_exists_and_is_executable_with_correct_contents():
    assert DEPLOY_SCRIPT.is_file(), (
        f"Expected deploy script {DEPLOY_SCRIPT} to exist, but it does not."
    )

    mode = DEPLOY_SCRIPT.stat().st_mode & 0o777
    assert mode == 0o755, (
        f"deploy_app.sh should have mode 755, but has {oct(mode)}."
    )

    expected_contents = (
        "#!/bin/bash\n"
        "while true; do\n"
        '    echo "Deploying..." >> /home/user/deployment/app.log\n'
        "    sleep 60\n"
        "done\n"
    )
    with DEPLOY_SCRIPT.open("r", encoding="utf-8") as fp:
        actual = fp.read()
    assert (
        actual == expected_contents
    ), "deploy_app.sh contents do not match the expected template."


def test_pid_and_snapshot_files_do_not_yet_exist():
    assert not PID_FILE.exists(), (
        f"{PID_FILE} already exists; the exercise expects it to be absent at start."
    )
    assert not SNAPSHOT_FILE.exists(), (
        f"{SNAPSHOT_FILE} already exists; the exercise expects it to be absent at start."
    )


def test_no_deploy_app_process_running():
    pids = _collect_running_deploy_pids()
    assert not pids, (
        "Found running instances of deploy_app.sh (PIDs: {}) but none should be running "
        "before the student launches the long-running helper.".format(", ".join(map(str, pids)))
    )