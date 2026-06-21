FROM ubuntu:22.04

# Labels
LABEL Author="devsecops-task-preparer"
LABEL Description="Container for semantic versioning & changelog policy task"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -eux && \
    # Install Python and pytest
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/* && \
    # Create initial project structure in /home/user/project
    mkdir -p /home/user/project/scripts && \
    # VERSION file
    echo '1.2.3' > /home/user/project/VERSION

# Initial CHANGELOG.md
RUN cat > /home/user/project/CHANGELOG.md <<'EOF'
## [1.2.3] - 2023-11-01
### Fixed
- initial release
EOF

# bump_patch.sh helper
RUN cat > /home/user/project/scripts/bump_patch.sh <<'EOS'
#!/usr/bin/env bash
# Helper to bump patch version and update changelog.
# Usage: bump_patch.sh "<changelog entry>"
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 \"<changelog entry>\"" >&2
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_ROOT="$( dirname "${SCRIPT_DIR}" )"

VERSION_FILE="${PROJECT_ROOT}/VERSION"
CHANGELOG_FILE="${PROJECT_ROOT}/CHANGELOG.md"

# Read current version
old_version="$(tr -d ' \t\n\r' < "${VERSION_FILE}")"
IFS='.' read -r major minor patch <<< "${old_version}"
new_patch=$((patch + 1))
new_version="${major}.${minor}.${new_patch}"

# Update VERSION file
printf '%s\n' "${new_version}" > "${VERSION_FILE}"

# Prepare new changelog section
today="2024-01-15"
line1="## [${new_version}] - ${today}"
line2="### Fixed"
line3="- $1"

{
    printf '%s\n' "${line1}"
    printf '%s\n' "${line2}"
    printf '%s\n' "${line3}"
    printf '\n'
} > "${CHANGELOG_FILE}.new"

# Append existing changelog
cat "${CHANGELOG_FILE}" >> "${CHANGELOG_FILE}.new"
mv "${CHANGELOG_FILE}.new" "${CHANGELOG_FILE}"

# Output summary
echo "Bumped to ${new_version}"
EOS

RUN chmod +x /home/user/project/scripts/bump_patch.sh && \
    chmod 755 /home/user && \
    # Ensure non-root users can modify the repo during testing
    chmod -R a+rwX /home/user/project

# Help information (as comments)
# This container sets up an initial repository in /home/user/project.
# Students must execute a single command to bump the patch version using
# the provided scripts/bump_patch.sh helper while conforming to strict
# changelog formatting rules. Pytest is pre-installed for automated checks.