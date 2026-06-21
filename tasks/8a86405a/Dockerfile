FROM ubuntu:22.04

# Install Python, pip, pytest, and prepare dataset structure
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    DATA_DIR="/home/user/data" && \
    ORIG_DIR="${DATA_DIR}/original" && \
    WORK_DIR="${DATA_DIR}/working" && \
    mkdir -p "${ORIG_DIR}" "${WORK_DIR}" && \
    printf "id,value\n1,42\n" > "${ORIG_DIR}/train_set.csv" && \
    printf "id,value\n1,24\n" > "${ORIG_DIR}/test_set.csv" && \
    chmod 644 "${ORIG_DIR}/train_set.csv" "${ORIG_DIR}/test_set.csv" && \
    chmod 777 "${WORK_DIR}" && \
    chmod 755 "${ORIG_DIR}" && \
    mkdir -p /home/user && chmod 755 /home/user && \
    chmod 755 "${DATA_DIR}"

ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="example_builder"
LABEL Description="Environment for symlink creation task with pytest pre-installed."

# Default runscript behavior
CMD sh -c "echo 'Container for the symlink creation task. Use it with an agent runner or shell.'"