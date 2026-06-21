FROM ubuntu:22.04

# Help text
# This container provides the initial state for the backup manifest exercise.
# It contains Python 3 with pytest pre-installed for automated grading.
# The required manifest file is located at:
#     /home/user/backup_test/input/manifest.log
# Students should create output files in /home/user/backup_test/output/

LABEL Author="backup-operator-exercise" \
      Description="Base image for backup manifest parsing task"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN useradd -m -d /home/user user || true

RUN set -e && \
    BASE_DIR="/home/user/backup_test" && \
    INPUT_DIR="${BASE_DIR}/input" && \
    mkdir -p "${INPUT_DIR}" && \
    chmod 755 /home /home/user || true && \
    chmod 755 "${BASE_DIR}" "${INPUT_DIR}"

RUN cat > /home/user/backup_test/input/manifest.log <<'EOF'
2024-06-01 01:00:00 /var/www/html/index.html 2048 OK
2024-06-01 01:00:05 /var/log/syslog 1048576 OK
2024-06-01 01:00:10 /etc/passwd 4096 FAILED
2024-06-01 01:00:15 /home/user/data/report.pdf 8192 OK
2024-06-01 01:00:20 /home/user/secret/notes.txt 1234 FAILED
EOF

RUN chmod 644 /home/user/backup_test/input/manifest.log

CMD ["bash"]