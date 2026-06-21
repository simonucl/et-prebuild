FROM ubuntu:22.04

# Basic packages and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Create non-root user “user” with home /home/user
RUN useradd -m -s /bin/bash user

# Prepare the initial data directory
RUN install -d -o user -g user /home/user/data

RUN python3 - << 'PY'
import pathlib

files = [
    (
        "/home/user/data/latin1_report.txt",
        "latin-1",
        "Café, crème brûlée, coöperate\nÅngström unit\n",
    ),
    (
        "/home/user/data/shiftjis_notes.txt",
        "shift_jis",
        "こんにちは\nバックアップ\n",
    ),
    (
        "/home/user/data/windows1252_legacy.txt",
        "windows-1252",
        "“Smart quotes” and € symbol\nOld file\n",
    ),
]

for path, enc, text in files:
    pathlib.Path(path).write_bytes(text.encode(enc))
PY

# Ensure “user” owns everything under /home/user
RUN chown -R user:user /home/user

# Environment settings
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"

# Labels
LABEL Author="OpenAI Assistant"
LABEL Description="Environment for mixed-encoding to UTF-8 conversion task. Includes legacy-encoded source files and pytest."