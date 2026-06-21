FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi

RUN PROFILER_DIR="/home/user/profiler" && \
    mkdir -p "${PROFILER_DIR}" && \
    printf 'PID\tCommand\tCPU%%\n101\tnginx\t12.3\n202\tpostgres\t43.1\n303\tredis\t5.6\n' \
        > "${PROFILER_DIR}/cpu.log" && \
    printf 'PID\tCommand\tMEM%%\n101\tnginx\t84\n202\tpostgres\t256\n303\tredis\t37\n' \
        > "${PROFILER_DIR}/mem.log" && \
    chown -R user:user /home/user && \
    chmod 755 /home/user "${PROFILER_DIR}" && \
    chmod 644 "${PROFILER_DIR}/cpu.log" "${PROFILER_DIR}/mem.log"

LABEL Author="performance-engineer-task-setup"