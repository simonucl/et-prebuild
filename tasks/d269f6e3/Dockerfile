FROM ubuntu:22.04

# Labels
LABEL Author="task-preparer"
LABEL Description="Container prepared for the symlink deployment exercise"

RUN set -eux && \
    # Update apt cache and install Python + pip
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    # Install pytest for the test harness
    pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state expected by the test suite
# Create the mandatory release directory (and parents) that must
# exist before the learner runs the task.
RUN RELEASE_DIR="/home/user/www/releases/2023-01-15" && \
    mkdir -p "${RELEASE_DIR}" && \
    # Place a placeholder file so the directory is non-empty
    echo "<html><body>Release placeholder</body></html>" > "${RELEASE_DIR}/index.html" && \
    # Make sure the learner—who will run unprivileged—can write inside
    # /home/user in order to create the symlink and log file.
    chmod -R 0777 /home/user

# Set proper permissions on /home/user
RUN chmod 755 /home/user

# Default command
CMD ["/bin/bash", "-c", "echo 'This container sets up the initial state for the symlink deployment exercise.' && echo 'Invoke your commands inside an interactive shell.'"]