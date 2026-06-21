# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="localization-task-setup" \
      Description="Base image for localization task with initial template and pytest installed."

# Ensure non-interactive apt and install dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir pytest

# Create initial workspace expected by the tests
RUN mkdir -p /home/user/localization/templates

# Create the messages.pot template using a heredoc
RUN cat > /home/user/localization/templates/messages.pot <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: 1.2\n"
"Report-Msgid-Bugs-To: you@example.com\n"
"POT-Creation-Date: 2023-06-30 09:00+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Language-Team: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
EOF

# Ensure correct permissions (directories 755, files 644)
RUN chmod 755 /home/user /home/user/localization /home/user/localization/templates && \
    chmod 644 /home/user/localization/templates/messages.pot

# Environment variables from %environment
ENV PYTHONIOENCODING=UTF-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# This container is set up for the localization engineering task.