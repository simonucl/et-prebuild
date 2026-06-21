FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create directory structure for the CI logs
RUN mkdir -p /home/user/mobile_ci/logs && \
    mkdir -p /home/user/mobile_ci/reports

# Populate log file: 2023-08-01
RUN cat <<'EOF' > /home/user/mobile_ci/logs/build_2023-08-01_c1345.log
[INFO] Start build: c1345
[INFO] Step compile: SUCCESS in 45000ms
[INFO] Step test: SUCCESS in 30000ms
[INFO] Step package: SUCCESS in 10000ms
[INFO] Build finished with status: SUCCESS
Duration: 85000ms
EOF

# Populate log file: 2023-08-02
RUN cat <<'EOF' > /home/user/mobile_ci/logs/build_2023-08-02_c1346.log
[INFO] Start build: c1346
[INFO] Step compile: SUCCESS in 43000ms
[INFO] Step test: SUCCESS in 28000ms
[INFO] Step package: SUCCESS in 9000ms
[INFO] Build finished with status: SUCCESS
Duration: 80000ms
EOF

# Populate log file: 2023-08-03
RUN cat <<'EOF' > /home/user/mobile_ci/logs/build_2023-08-03_c1347.log
[INFO] Start build: c1347
[INFO] Step compile: SUCCESS in 46000ms
[INFO] Step test: SUCCESS in 31000ms
[INFO] Step package: SUCCESS in 9500ms
[INFO] Build finished with status: SUCCESS
Duration: 86500ms
EOF

# Populate log file: 2023-08-04
RUN cat <<'EOF' > /home/user/mobile_ci/logs/build_2023-08-04_c1348.log
[INFO] Start build: c1348
[INFO] Step compile: SUCCESS in 47000ms
[INFO] Step test: FAILURE in 32000ms
[INFO] Step package: SKIPPED
[INFO] Build finished with status: FAILURE
Duration: 79000ms
EOF

# Permissions
RUN chmod -R a+rX /home/user/mobile_ci/logs
RUN chmod 0777 /home/user/mobile_ci/reports

# Metadata
LABEL Author="Mobile-CI-Setup"
LABEL Description="Provides initial log data and environment for the Mobile CI weekly report task."