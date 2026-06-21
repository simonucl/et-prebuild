# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial project workspace
RUN mkdir -p /home/user/project/data/raw

RUN cat > /home/user/project/data/raw/report1.txt <<'EOF'
Q1 RESULTS
CONFIDENTIAL
Numbers …
EOF

RUN cat > /home/user/project/data/raw/report2.txt <<'EOF'
Public release – nothing confidential.
EOF

RUN cat > /home/user/project/data/raw/secret_notes.txt <<'EOF'
CONFIDENTIAL
Internal roadmap …
EOF

RUN cat > /home/user/project/data/raw/analysis.txt <<'EOF'
Executive summary
CONFIDENTIAL data enclosed …
EOF

RUN cat > /home/user/project/data/raw/draft.log <<'EOF'
[log lines]
EOF

RUN chmod -R a+rwX /home/user

# From %environment — chmod must be a command, not ENV
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV PYTHONIOENCODING=UTF-8

# Labels from %labels
LABEL Author="Automation-Workflow Exercise"
LABEL Description="Container image for the “CONFIDENTIAL file-copy” workflow task."