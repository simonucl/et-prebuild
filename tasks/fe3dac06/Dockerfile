FROM ubuntu:22.04

# Help text
# This container provides the dependencies and initial filesystem state
# for the “SQLite file-indexing” exercise. It includes:
#   • sqlite3 CLI
#   • Python 3 with pytest
# The directory /home/user/projects exists and is writable, but contains
# no database or log files so that students can complete the assignment
# from a clean slate.

LABEL Author="ChatGPT"
LABEL Description="Environment for SQLite file-indexing exercise (pytest pre-checks only)"

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
    && pip3 install --no-cache-dir pytest \
    && mkdir -p /home/user/projects \
    && chmod 0777 /home/user \
    && chmod 0777 /home/user/projects