FROM ubuntu:22.04

# %help section
# This container supplies the initial state for the Mobile CI failure-report exercise.
# Includes /home/user/mobile_ci/build_pipeline.log and pytest installed for grading.
# Learners should create /home/user/mobile_ci/reports/failure_report_20230821.txt.
# Ensure solutions run without root privileges.

ENV PATH="/usr/local/bin:$PATH"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/mobile_ci

RUN cat >/home/user/mobile_ci/build_pipeline.log <<'LOGEOF'
[2023-08-21 10:01:03] BUILD 101: core - SUCCESS
[2023-08-21 10:05:47] BUILD 102: ui - FAILED
[2023-08-21 10:12:11] BUILD 103: networking - SUCCESS
[2023-08-21 10:15:29] BUILD 104: feature-auth - FAILED
[2023-08-21 10:22:58] BUILD 105: feature-payments - FAILED
[2023-08-21 10:30:42] BUILD 106: analytics - SUCCESS
[2023-08-21 10:33:27] BUILD 107: push-notifications - SUCCESS
[2023-08-21 10:38:55] BUILD 108: ui - FAILED
LOGEOF

RUN chmod -R 0755 /home/user