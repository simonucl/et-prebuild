# Converted from Apptainer .def
FROM ubuntu:22.04

# %post section
RUN set -e && \
    echo "Updating package list and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# %environment section
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV PYTHONIOENCODING="utf-8"

# Ensure permissions (Apptainer %environment had chmod)
RUN chmod 755 /home/user

# %labels section
LABEL Author="Generated for credential-rotation exercise"
LABEL Description="Baseline image with Python, pytest, and writable /home/user"

# %runscript section (container default command)
CMD echo "This container provides the tooling required for the credential-rotation exercise." && \
    echo "Invoke an interactive shell with:  docker run -it <image> /bin/bash"