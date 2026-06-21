FROM ubuntu:22.04

# Author: localization-task-setup
# Description: Container for Localization Engineer exercise – initial state prepared
# Help:
# This Apptainer image contains the initial filesystem state and dependencies
# for the “Localization Engineer: Update French Translations & Record API-style
# Tests With curl” exercise.

ENV PATH="/home/user/.local/bin:$PATH"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/project/locales

RUN cat <<'EOF' >/home/user/project/locales/en.json
{"hello":"Hello","bye":"Goodbye"}
EOF

RUN cat <<'EOF' >/home/user/project/locales/fr.json
{"hello":"Bonjour","bye":"Au revoir","obsolete":"obsolète"}
EOF

RUN chmod -R a+rwX /home/user/project

RUN chmod 755 /home/user