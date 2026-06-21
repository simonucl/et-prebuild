FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Exercise Autogen"
LABEL Description="Base image for the Europe/Berlin TZ & en_US.UTF-8 locale task (pytest included)"

# Post installation commands
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata && \
    # Enable and generate the UTF-8 locale that will later be used by the user
    sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    # Install pytest for the task's test-runner
    pip3 install --no-cache-dir pytest && \
    # Create an unprivileged account "user" (UID/GID 1000) with /home/user
    groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true && \
    # Provide the user with a standard .bashrc (without the exercise line)
    cp /etc/skel/.bashrc /home/user/.bashrc && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default entrypoint: an interactive shell
CMD ["/bin/bash"]