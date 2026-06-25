#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
export HOME=/home/user

if python3 - <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ["HOME"] = "/home/user"

KEYS = [
    "user.name",
    "user.email",
    "pull.ff",
    "core.sshCommand",
    "gpg.format",
    "user.signingKey",
    "commit.gpgSign",
    "tag.gpgSign",
    "commit.template",
    "commit.cleanup",
    "receive.fsckObjects",
    "transfer.fsckObjects",
    "push.followTags",
]

REPOS = [
    {
        "path": "/home/user/work/clientA/service",
        "branch": "release/1.8",
        "remote": "https://git.corp.example/clientA/service.git",
        "profiles": ["clienta", "release"],
        "values": {
            "user.name": "Jordan Lee",
            "user.email": "jordan.lee@clienta.example",
            "pull.ff": "only",
            "core.sshCommand": "ssh -i ~/.ssh/clienta_ed25519 -F /dev/null",
            "gpg.format": "ssh",
            "user.signingKey": "/home/user/.ssh/clienta_signing.pub",
            "commit.gpgSign": "true",
            "tag.gpgSign": "true",
            "commit.template": None,
            "commit.cleanup": "scissors",
            "receive.fsckObjects": None,
            "transfer.fsckObjects": None,
            "push.followTags": "true",
        },
    },
    {
        "path": "/home/user/work/clientA/security/gateway",
        "branch": "hotfix/CVE-2026-4242",
        "remote": "ssh://git@git.corp.example:2222/security/gateway.git",
        "profiles": ["clienta", "security", "hotfix"],
        "values": {
            "user.name": "Jordan Lee",
            "user.email": "jordan.security@clienta.example",
            "pull.ff": "only",
            "core.sshCommand": "ssh -i ~/.ssh/security_ed25519 -F /dev/null",
            "gpg.format": "ssh",
            "user.signingKey": "/home/user/.ssh/clienta_signing.pub",
            "commit.gpgSign": "true",
            "tag.gpgSign": None,
            "commit.template": "/home/user/.config/git/hotfix-template.txt",
            "commit.cleanup": "scissors",
            "receive.fsckObjects": "true",
            "transfer.fsckObjects": "true",
            "push.followTags": None,
        },
    },
    {
        "path": "/home/user/work/vendor/security-mirror",
        "branch": "main",
        "remote": "https://git.corp.example/security/mirror.git",
        "profiles": ["default", "security"],
        "values": {
            "user.name": "Jordan Lee",
            "user.email": "jordan.security@clienta.example",
            "pull.ff": "only",
            "core.sshCommand": "ssh -i ~/.ssh/security_ed25519 -F /dev/null",
            "gpg.format": None,
            "user.signingKey": None,
            "commit.gpgSign": None,
            "tag.gpgSign": None,
            "commit.template": None,
            "commit.cleanup": None,
            "receive.fsckObjects": "true",
            "transfer.fsckObjects": "true",
            "push.followTags": None,
        },
    },
    {
        "path": "/home/user/work/personal/notes",
        "branch": "hotfix/private",
        "remote": "https://git.personal.example/jordan/notes.git",
        "profiles": ["default"],
        "values": {
            "user.name": "Jordan Lee",
            "user.email": "jordan@personal.example",
            "pull.ff": "only",
            "core.sshCommand": None,
            "gpg.format": None,
            "user.signingKey": None,
            "commit.gpgSign": None,
            "tag.gpgSign": None,
            "commit.template": None,
            "commit.cleanup": None,
            "receive.fsckObjects": None,
            "transfer.fsckObjects": None,
            "push.followTags": None,
        },
    },
]

EXPECTED_REPORT = {
    "default": {
        "user.name": "Jordan Lee",
        "user.email": "jordan@personal.example",
        "pull.ff": "only",
    },
    "includes": [
        {"name": "clienta", "path": "/home/user/.config/git/clienta.inc"},
        {"name": "security", "path": "/home/user/.config/git/security.inc"},
        {"name": "release", "path": "/home/user/.config/git/release.inc"},
        {"name": "hotfix", "path": "/home/user/.config/git/hotfix.inc"},
    ],
    "repositories": [
        {
            "path": repo["path"],
            "branch": repo["branch"],
            "profiles": repo["profiles"],
            **repo["values"],
        }
        for repo in REPOS
    ],
}

def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

def git(args, missing_ok=False):
    proc = subprocess.run(
        ["git", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if missing_ok and proc.returncode == 1:
        return None
    if proc.returncode != 0:
        fail(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.rstrip("\n")

def git_repo(repo, args, missing_ok=False):
    return git(["-C", repo, *args], missing_ok=missing_ok)

if not Path("/home/user/.gitconfig").is_file():
    fail("/home/user/.gitconfig is missing")

for path in [
    "/home/user/.config/git/clienta.inc",
    "/home/user/.config/git/security.inc",
    "/home/user/.config/git/release.inc",
    "/home/user/.config/git/hotfix.inc",
    "/home/user/.config/git/hotfix-template.txt",
    "/home/user/.ssh/clienta_ed25519",
    "/home/user/.ssh/security_ed25519",
    "/home/user/.ssh/clienta_signing.pub",
]:
    if not Path(path).exists():
        fail(f"required file is missing: {path}")

include_output = git(["config", "--global", "--get-regexp", r"^includeIf\..*\.path$"])
required_global = [
    [
        "includeif.gitdir:~/work/clientA/**.path ~/.config/git/clienta.inc",
        "includeif.gitdir:~/work/clientA/**.path /home/user/.config/git/clienta.inc",
    ],
    [
        "includeif.hasconfig:remote.*.url:*://*git.corp.example*/security/**.path ~/.config/git/security.inc",
        "includeif.hasconfig:remote.*.url:*://*git.corp.example*/security/**.path /home/user/.config/git/security.inc",
    ],
]
for accepted in required_global:
    if not any(line in include_output for line in accepted):
        fail(f"missing or incorrect global conditional include; accepted forms: {accepted}")

clienta_includes = git(["config", "--file", "/home/user/.config/git/clienta.inc", "--get-regexp", r"^includeIf\..*\.path$"])
for expected in [
    "includeif.onbranch:release/**.path ~/.config/git/release.inc",
    "includeif.onbranch:release/**.path /home/user/.config/git/release.inc",
]:
    if expected in clienta_includes:
        break
else:
    fail("clienta profile must include release profile with onbranch:release/**")
for expected in [
    "includeif.onbranch:hotfix/**.path ~/.config/git/hotfix.inc",
    "includeif.onbranch:hotfix/**.path /home/user/.config/git/hotfix.inc",
]:
    if expected in clienta_includes:
        break
else:
    fail("clienta profile must include hotfix profile with onbranch:hotfix/**")

for repo in REPOS:
    repo_path = repo["path"]
    if not (Path(repo_path) / ".git" / "config").is_file():
        fail(f"{repo_path} is no longer a Git repository")
    if git_repo(repo_path, ["branch", "--show-current"]) != repo["branch"]:
        fail(f"{repo_path} is not on branch {repo['branch']}")
    if git_repo(repo_path, ["config", "--local", "--get", "remote.origin.url"]) != repo["remote"]:
        fail(f"{repo_path} origin URL was changed")
    forbidden = git_repo(
        repo_path,
        ["config", "--local", "--get-regexp", r"^(user\.|pull\.ff$|core\.sshcommand$|gpg\.|commit\.|tag\.|receive\.|transfer\.|push\.followtags$)"],
        missing_ok=True,
    )
    if forbidden:
        fail(f"{repo_path} contains forbidden local profile settings: {forbidden}")
    for key, expected in repo["values"].items():
        actual = git_repo(repo_path, ["config", "--includes", "--get", key], missing_ok=True)
        if actual != expected:
            fail(f"{repo_path} expected {key}={expected!r}, got {actual!r}")

report_path = Path("/home/user/git_profile_report.json")
if not report_path.is_file():
    fail("/home/user/git_profile_report.json is missing")
raw_report = report_path.read_bytes()
if not raw_report.endswith(b"\n") or raw_report.count(b"\n") != 1:
    fail("report must be one minified JSON line with exactly one trailing newline")
if b": " in raw_report or b", " in raw_report:
    fail("report must be minified JSON without spaces after separators")
try:
    report = json.loads(raw_report)
except json.JSONDecodeError as exc:
    fail(f"report is not valid JSON: {exc}")
if list(report.keys()) != ["default", "includes", "repositories"]:
    fail("report top-level keys are missing or in the wrong order")
if report != EXPECTED_REPORT:
    fail("report content does not match the required effective profile summary")
PY
then
  reward=1
fi

echo "$reward" > /logs/verifier/reward.txt
exit 0
