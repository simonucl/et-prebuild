FROM ubuntu:22.04

# Update package index and install Python/pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare initial on-disk state for the assignment
RUN mkdir -p /home/user/restore-tests

# step1.md (line 1 ends with TWO spaces)
RUN cat > /home/user/restore-tests/step1.md <<'EOF'
Restore Step 1  
Run backup command.
EOF

# step2.md
RUN cat > /home/user/restore-tests/step2.md <<'EOF'
Restore Step 2
Verify backup.
EOF

# Make everything user-writable so the agent (non-root) can modify/create files
RUN chmod -R a+rwX /home/user

ENV HOME=/home/user

LABEL Author="backup-operator-task-preparer"
LABEL Description="Container for trailing whitespace detection task (Apptainer)"

# Help:
# This container provides the initial state for the "trailing whitespace"
# Markdown scanning assignment.  It contains two Markdown files under
# /home/user/restore-tests/ exactly as described in the problem statement,
# and pytest is installed for automated grading.