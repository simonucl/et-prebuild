FROM ubuntu:22.04

# Author: ChatGPT
# Description: Starter image for the user-login micro-service exercise. Provides Python, pytest, sqlite3 and guarantees that /home/user/dev_data/ exists and is writable when any Python process starts.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
        locales && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/dev_data && \
    chmod 0777 /home/user/dev_data && \
    mkdir -p /usr/local/lib/python3.10

RUN cat << 'PYTHON_EOF' > /usr/local/lib/python3.10/sitecustomize.py
"""
sitecustomize.py – executed automatically by Python on start-up.

Its sole purpose is to make sure that /home/user/dev_data exists and is
writable by the current (non-root) user, regardless of host bind mounts.
"""
import os
import stat

TARGET = "/home/user/dev_data"

try:
    # Create the directory tree if it does not already exist.
    os.makedirs(TARGET, exist_ok=True)

    # Ensure the user has write permission on the directory.
    st = os.stat(TARGET)
    if not (st.st_mode & stat.S_IWUSR):
        os.chmod(TARGET, st.st_mode | stat.S_IWUSR)
except Exception:
    # Do not impede interpreter start-up under any circumstances.
    pass
PYTHON_EOF

RUN chmod 0644 /usr/local/lib/python3.10/sitecustomize.py

RUN chmod 755 /home/user

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:$PATH

# Equivalent of runscript
CMD echo "Container for the user-login micro-service exercise." && \
    echo "Use \`docker run <image> <command>\` to run arbitrary commands."