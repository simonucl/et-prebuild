FROM ubuntu:22.04

# Help / labels
# Author: BenchmarkSetup
# Description: Initial container state for benchmarking assignment
LABEL Author="BenchmarkSetup"
LABEL Description="Initial container state for benchmarking assignment"

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user || true

RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        ca-certificates; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN set -eux; \
    PROJECT_ROOT="/home/user/project"; \
    SRC_DIR="${PROJECT_ROOT}/src"; \
    UTILS_DIR="${SRC_DIR}/utils"; \
    mkdir -p "${UTILS_DIR}"; \
    chmod 0777 "${PROJECT_ROOT}"

RUN set -eux; \
    SRC_DIR="/home/user/project/src"; \
    : > "${SRC_DIR}/__init__.py"; \
    chmod 0644 "${SRC_DIR}/__init__.py"

RUN cat > "/home/user/project/src/main.py" <<'EOF'
print('Hello world')
EOF

RUN chmod 0644 "/home/user/project/src/main.py"

RUN cat > "/home/user/project/src/utils/helpers.py" <<'EOF'
def helper():
    pass
EOF

RUN chmod 0644 "/home/user/project/src/utils/helpers.py"

RUN cat > "/home/user/project/README.md" <<'EOF'
# Project Title

This is a sample project used for benchmarking demonstration.
It contains a small source tree with a classic Hello world program.
The benchmark task will measure the performance of a few maintenance
operations such as directory listing, compression, and line counting.
EOF

RUN chmod 0644 "/home/user/project/README.md"

CMD echo "Container for benchmarking task. Execute the assignment steps in an interactive shell."