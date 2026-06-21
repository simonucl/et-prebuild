# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic tools and Python/pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Directory layout expected by the exercise
# ------------------------------------------------------------------
RUN mkdir -p /home/user/research_logs && \
    mkdir -p /home/user/analysis

# ------------------------------------------------------------------
# Pre-existing log files
# ------------------------------------------------------------------
RUN cat > /home/user/research_logs/experiment_A.log <<'EOF'
[2023-04-12 09:55:03] INFO  DataLoad: Starting batch 17
[2023-04-12 10:05:11] WARN  DataLoad: Incomplete record encountered
[2023-04-12 10:17:45] ERROR DataLoad: Null pointer exception
[2023-04-12 11:02:33] INFO  PreProcess: Normalization done
[2023-04-12 11:45:12] WARN  DataLoad: Timeout on socket 3
[2023-04-12 12:05:35] ERROR Model: Overflow in layer 9
[2023-04-12 12:15:07] INFO  DataLoad: Batch finished
EOF

RUN cat > /home/user/research_logs/experiment_B.log <<'EOF'
[2023-04-12 09:40:10] INFO  DataLoad: Starting batch 02
[2023-04-12 10:12:21] WARN  DataLoad: Missing value filled
[2023-04-12 10:55:09] ERROR DataLoad: Index out of range
[2023-04-12 11:12:41] INFO  Train: Epoch 1 done
[2023-04-12 11:59:59] WARN  DataLoad: Disk read latency high
[2023-04-12 12:08:10] ERROR Optimizer: Divergence detected
EOF

RUN cat > /home/user/research_logs/experiment_control.log <<'EOF'
[2023-04-12 10:01:01] INFO  Monitor: checksum validated
[2023-04-12 10:31:18] INFO  Monitor: checksum validated
[2023-04-12 11:05:22] INFO  Monitor: heartbeat ok
[2023-04-12 11:46:45] INFO  Monitor: checksum validated
[2023-04-12 12:02:32] INFO  Monitor: shutdown
EOF

# ------------------------------------------------------------------
# Permissions
# ------------------------------------------------------------------
RUN chmod 644 /home/user/research_logs/*.log && \
    chmod 755 /home/user/research_logs && \
    chmod 777 /home/user/analysis && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="alert-digest-setup" \
      Description="Environment for the alert-digest bio-informatics log exercise"