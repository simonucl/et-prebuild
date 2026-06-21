# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install the software needed for both the learner and the tests
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        diffutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# pytest is required by the automated grading harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create the initial filesystem state for the exercise
# ------------------------------------------------------------------
# Ensure the base directory exists and is accessible
RUN mkdir -p /home/user/backup && \
    mkdir -p /home/user/updates

# Old snapshot
RUN cat > /home/user/backup/disk_usage_report_old.txt <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       40G   30G  8G   79% /
/dev/sdb1       100G  60G  35G  65% /data
tmpfs           2.0G  0    2.0G  0% /dev/shm
EOF

# New snapshot
RUN cat > /home/user/backup/disk_usage_report_new.txt <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       40G   28G  10G  72% /
/dev/sdb1       100G  55G  40G  60% /data
tmpfs           2.0G  0    2.0G  0% /dev/shm
EOF

# ------------------------------------------------------------------
# Permissions
# ------------------------------------------------------------------
# Make sure the learner (non-root at runtime) can work with the data.
RUN chmod 755 /home/user && \
    chmod 755 /home/user/backup && \
    chmod 777 /home/user/updates && \
    chmod 644 /home/user/backup/disk_usage_report_old.txt && \
    chmod 644 /home/user/backup/disk_usage_report_new.txt

# Labels
LABEL Author="Apptainer Prep Bot" \
      Purpose="Initial state for disk usage diff exercise"