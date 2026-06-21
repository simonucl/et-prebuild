# syntax=docker/dockerfile:1
# Author: MobileBuildEng
# Description: Apptainer image that sets up initial Android CI log files and installs pytest.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/mobile_ci/logs

RUN cat > /home/user/mobile_ci/logs/build_2024-06-01.log <<'EOF'
=== BUILD START ===
JobID: 1001
Variant: debug
Timestamp: 2024-06-01T10:15:00Z
Status: SUCCESS
=== BUILD END ===

=== BUILD START ===
JobID: 1002
Variant: release
Timestamp: 2024-06-01T11:00:00Z
Status: FAILURE
Reason: Unit tests failed
=== BUILD END ===
EOF

RUN cat > /home/user/mobile_ci/logs/build_2024-06-02.log <<'EOF'
=== BUILD START ===
JobID: 1003
Variant: debug
Timestamp: 2024-06-02T09:05:00Z
Status: FAILURE
Reason: Gradle compilation error
=== BUILD END ===

=== BUILD START ===
JobID: 1004
Variant: release
Timestamp: 2024-06-02T14:20:00Z
Status: SUCCESS
=== BUILD END ===
EOF

RUN cat > /home/user/mobile_ci/logs/build_2024-06-03.log <<'EOF'
=== BUILD START ===
JobID: 1005
Variant: release
Timestamp: 2024-06-03T08:40:00Z
Status: FAILURE
Reason: Lint violations
=== BUILD END ===
EOF

RUN chmod -R 0777 /home/user/mobile_ci

RUN chmod 755 /home/user