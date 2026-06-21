# test_initial_state.py
#
# This test-suite asserts that the workstation is in a **clean initial state**
# before the student performs any actions.  None of the artefacts that the
# exercise later demands (systemd unit/timer, cron file, summary log) should
# exist yet.  If any of them are already present, the environment is considered
# “dirty” and the test will fail with an explanatory message.
#
# NOTE: A failing test here means the starting environment is **incorrect**;
#       it does NOT mean the student has done something wrong.

import os
import stat
import textwrap
import pytest

HOME = "/home/user"

# Mapping of *final* artefacts → their expected contents (byte-exact, incl. LF)
EXPECTED_ARTEFACTS = {
    f"{HOME}/.config/systemd/user/k8s-manifest-sync.service": textwrap.dedent("""\
        [Unit]
        Description=Sync Kubernetes manifests from local directory

        [Service]
        Type=oneshot
        WorkingDirectory=/home/user/k8s-manifests
        ExecStart=/usr/bin/kubectl apply -k .

        [Install]
        WantedBy=default.target
        """),
    f"{HOME}/.config/systemd/user/k8s-manifest-sync.timer": textwrap.dedent("""\
        [Unit]
        Description=Run k8s-manifest-sync every 5 minutes

        [Timer]
        OnCalendar=*:0/5
        Unit=k8s-manifest-sync.service

        [Install]
        WantedBy=timers.target
        """),
    f"{HOME}/cron/k8s_cleanup": "0 2 * * * /usr/bin/find /home/user/k8s-manifests/tmp -type f -mtime +7 -delete\n",
    f"{HOME}/manifest_automation_setup.log": textwrap.dedent("""\
        [OK] Created /home/user/.config/systemd/user/k8s-manifest-sync.service
        [OK] Created /home/user/.config/systemd/user/k8s-manifest-sync.timer
        [OK] Created /home/user/cron/k8s_cleanup
        [OK] systemd user daemon reloaded
        [OK] k8s-manifest-sync.timer enabled
        """),
}

@pytest.mark.parametrize("path,expected_content", EXPECTED_ARTEFACTS.items())
def test_final_files_do_not_exist_yet(path, expected_content):
    """
    Assert that none of the files required *after* the task are present *before*
    the student starts.  Presence of any of these files indicates the base
    image / workspace is already polluted with a solution or partial solution.
    """
    assert not os.path.exists(path), (
        f"File {path} should NOT exist before the student begins the task, "
        "but it is already present.  Please clean the workspace."
    )

@pytest.mark.parametrize("dir_path", [
    f"{HOME}/.config/systemd/user",
    f"{HOME}/cron",
])
def test_directories_may_exist_but_are_empty_of_target_files(dir_path):
    """
    The parent directories may pre-exist (that is fine), but if they do, they
    must not already contain any of the target artefacts.
    """
    if not os.path.isdir(dir_path):
        pytest.skip(f"Directory {dir_path} does not exist yet – that is fine.")

    # Collect any offending files that match the filenames we will later create.
    offending = []
    for filename in (
        "k8s-manifest-sync.service",
        "k8s-manifest-sync.timer",
        "k8s_cleanup",
    ):
        candidate = os.path.join(dir_path, filename)
        if os.path.exists(candidate):
            offending.append(candidate)

    assert not offending, (
        "The following files already exist but should not be present in the "
        f"initial state: {', '.join(offending)}"
    )

@pytest.mark.parametrize("path_mode_tuple", [
    (f"{HOME}/.config/systemd/user/k8s-manifest-sync.service", 0o600),
    (f"{HOME}/.config/systemd/user/k8s-manifest-sync.timer", 0o600),
    (f"{HOME}/cron/k8s_cleanup", 0o600),
    (f"{HOME}/manifest_automation_setup.log", 0o600),
])
def test_permissions_will_need_setting_later(path_mode_tuple):
    """
    This test is *informational only*.  It does not fail; it merely reminds the
    grader that permission checks will happen *after* creation.  If the file
    already exists (which would already have failed earlier), we would verify
    permissions.  Since the files must not exist yet, we skip.
    """
    path, _mode = path_mode_tuple
    if os.path.exists(path):
        perms = stat.S_IMODE(os.lstat(path).st_mode)
        pytest.skip(
            f"File {path} unexpectedly exists; permissions are {oct(perms)}"
        )
    else:
        pytest.skip(f"{path} does not exist yet – expected for initial state.")