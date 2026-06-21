# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic tooling
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create runtime user-space directory structure and seed data
# ------------------------------------------------------------------
RUN set -eux && \
    mkdir -p /home/user && \
    chmod 0777 /home /home/user && \
    mkdir -p /home/user/data/logs

# ------------------------------------------------------------------
# Populate the three raw authentication log files.
# ------------------------------------------------------------------
RUN cat >/home/user/data/logs/auth_2023-05-01.log <<'EOF'
2023-05-01T00:11:04Z user=alice action=login status=success ip=10.0.0.5
2023-05-01T01:45:33Z user=bob action=login status=failed ip=10.0.0.7
2023-05-01T02:17:54Z user=charlie action=login status=failed ip=10.0.0.9
2023-05-01T03:19:54Z user=alice action=logout status=success ip=10.0.0.5
EOF

RUN cat >/home/user/data/logs/auth_2023-05-02.log <<'EOF'
2023-05-02T04:22:10Z user=jdoe action=login status=failed ip=10.0.0.13
2023-05-02T05:24:10Z user=bob action=login status=success ip=10.0.0.7
2023-05-02T05:55:01Z user=erin action=login status=failed ip=10.0.0.11
EOF

RUN cat >/home/user/data/logs/auth_2023-05-03.log <<'EOF'
2023-05-03T06:30:00Z user=frank action=login status=failed ip=10.0.0.15
2023-05-03T07:31:00Z user=charlie action=login status=failed ip=10.0.0.9
2023-05-03T08:32:00Z user=jdoe action=login status=failed ip=10.0.0.13
2023-05-03T09:33:00Z user=george action=login status=success ip=10.0.0.20
EOF

# Ensure the files have UNIX line endings and correct permissions.
RUN chmod 0644 /home/user/data/logs/auth_2023-05-*.log

# Ensure final permissions on /home/user
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="task-setup" \
      Description="Environment for junior compliance-operations analyst task. Contains seeded log files and pytest."

# ------------------------------------------------------------------
# Default command
# ------------------------------------------------------------------
CMD ["/bin/bash"]