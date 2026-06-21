FROM ubuntu:22.04

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user that the grading framework can switch to
RUN useradd -m -s /bin/bash user

# ------------------------------------------------------------------
# Prepare the "remote share" directory with the staged configuration
# files required by the exercise.  These must be read-only to the
# student and must match the exact byte contents expected by the tests.
# ------------------------------------------------------------------
RUN REMOTE_DIR="/home/user/remote_share/configs" && \
    mkdir -p "${REMOTE_DIR}" && \
    printf "ENV=prod\n" > "${REMOTE_DIR}/app.conf" && \
    printf "version=2\n" > "${REMOTE_DIR}/settings.ini" && \
    printf "This is the remote config directory.\n" > "${REMOTE_DIR}/readme.txt" && \
    chown -R root:root /home/user/remote_share && \
    chmod 555 /home/user/remote_share && \
    chmod 555 /home/user/remote_share/configs && \
    chmod 444 /home/user/remote_share/configs/*

# Ensure the workspace directory expected to be created by the student
# does NOT exist at build time.
RUN rm -rf /home/user/support-sync

# Set permissions on /home/user
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD ["/bin/bash"]