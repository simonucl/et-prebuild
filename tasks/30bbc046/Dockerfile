FROM ubuntu:22.04

# Help section omitted (none provided)

ENV PYTHONIOENCODING=UTF-8

RUN set -e && \
    USER_HOME="/home/user" && \
    RAW_DIR="$USER_HOME/mock_api_data/raw" && \
    PROC_DIR="$USER_HOME/mock_api_data/processed" && \
    mkdir -p "$RAW_DIR" "$PROC_DIR" && \
    truncate -s 512 "$RAW_DIR/payload_01.json" && \
    truncate -s 256 "$RAW_DIR/payload_02.json" && \
    truncate -s 128 "$PROC_DIR/response_01.json" && \
    truncate -s 256 "$PROC_DIR/response_02.json" && \
    chown -R 1000:1000 "$USER_HOME"

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user