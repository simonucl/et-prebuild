#!/bin/bash
set -euo pipefail

export HOME=/home/user
mkdir -p /home/user/.config/git

cat > /home/user/.gitconfig <<'EOF'
[user]
	name = Riley Chen
	email = riley@personal.example
[includeIf "gitdir/i:~/work/research/**"]
	path = /home/user/.config/git/research.inc
[includeIf "hasconfig:remote.*.url:ssh://git.internal.example/security/**"]
	path = /home/user/.config/git/security.inc
EOF

cat > /home/user/.config/git/research.inc <<'EOF'
[user]
	email = riley.research@example.invalid
	signingKey = /home/user/.ssh/research_signing.pub
[core]
	sshCommand = ssh -i /home/user/.ssh/research_ro -F /dev/null
[gpg]
	format = ssh
[commit]
	gpgSign = true
[push]
	default = current
[includeIf "onbranch:review/**"]
	path = /home/user/.config/git/review.inc
EOF

cat > /home/user/.config/git/security.inc <<'EOF'
[user]
	email = riley.security@example.invalid
[commit]
	template = /home/user/.config/git/security-template.txt
[core]
	hooksPath = /home/user/.config/git/security-hooks
[transfer]
	fsckObjects = true
[fetch]
	fsckObjects = true
EOF

cat > /home/user/.config/git/review.inc <<'EOF'
[tag]
	gpgSign = true
[commit]
	cleanup = scissors
[advice]
	detachedHead = false
EOF

python3 - <<'PY'
import json
import subprocess

repos = [
    ("/home/user/work/research/model", ["research", "review"]),
    ("/home/user/work/Research/infra", ["research"]),
    ("/home/user/work/research/security-lib", ["research", "security", "review"]),
    ("/home/user/work/external/vendor-audit", ["default", "security"]),
    ("/home/user/work/personal/review-notes", ["default"]),
]
keys = [
    "user.name",
    "user.email",
    "core.sshCommand",
    "gpg.format",
    "user.signingKey",
    "commit.gpgSign",
    "tag.gpgSign",
    "commit.cleanup",
    "commit.template",
    "core.hooksPath",
    "transfer.fsckObjects",
    "fetch.fsckObjects",
    "push.default",
    "advice.detachedHead",
]

def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if proc.returncode:
        return None
    return proc.stdout.rstrip("\n")

report = {
    "default": {"user.name": "Riley Chen", "user.email": "riley@personal.example"},
    "includes": [
        {"name": "research", "path": "/home/user/.config/git/research.inc"},
        {"name": "security", "path": "/home/user/.config/git/security.inc"},
        {"name": "review", "path": "/home/user/.config/git/review.inc"},
    ],
    "repositories": [],
}

for repo, profiles in repos:
    item = {
        "path": repo,
        "branch": git(repo, "branch", "--show-current"),
        "profiles": profiles,
    }
    for key in keys:
        item[key] = git(repo, "config", "--includes", "--get", key)
    report["repositories"].append(item)

with open("/home/user/git-review-routing.json", "w", encoding="utf-8") as f:
    json.dump(report, f, separators=(",", ":"))
    f.write("\n")
PY
