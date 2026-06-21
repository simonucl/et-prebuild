FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Prep Bot"
LABEL Description="Container providing the initial state for the click-stream ETL exercise."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Update APT and install Python tooling
RUN set -e && \
    echo "Updating APT and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN echo "Installing pytest..." && \
    pip3 install --no-cache-dir --upgrade pip setuptools pytest

# Create initial raw data directory
RUN echo "Creating initial raw data directory and file structure..." && \
    mkdir -p /home/user/raw_data

# Create the raw events file
RUN cat > /home/user/raw_data/raw_events_20240315.jsonl <<'EOF'
{"event_id": 1001, "user_id": 55, "ts": "2024-05-28T12:34:56Z", "meta": "foo"}
{"event_id": 1002, "user_id": 56, "ts": "2024-05-28T12:35:56Z", "meta": "bar"}
{"event_id": 1003, "user_id": 57, "ts": "2024-05-28T12:36:56Z", "meta": "baz"}
{"event_id": 1004, "user_id": 58, "ts": "2024-05-28T12:37:56Z", "meta": "bat"}
EOF

# Ensure correct permissions (directories 755, file 644)
RUN chmod 755 /home/user && \
    chmod 755 /home/user/raw_data && \
    chmod 644 /home/user/raw_data/raw_events_20240315.jsonl

WORKDIR /home/user