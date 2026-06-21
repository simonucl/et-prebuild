FROM ubuntu:22.04

# Help documentation:
# This container provides a clean Ubuntu 22.04 environment for the
# "package diagnostics" exercise.  Pytest is pre-installed and the
# directory /home/user is ready for the learner to create the required
# artefacts.

# Update APT metadata and install system packages required for Python/pytest.
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness.
RUN pip3 install --no-cache-dir pytest

# Prepare the "user" home directory that the grading tests expect.
# We do NOT create /home/user/support here; the exercise must start
# without that directory or the pkg_diag.log file.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Minimal locale settings to avoid Python warnings.
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home/user

# Default to an interactive shell if the container is executed
# without explicit arguments.
CMD ["/bin/bash"]