FROM ubuntu:22.04

# Labels
LABEL Author="incident-prep"
LABEL Description="Initial workspace for INC123 log-handling exercise"

# Update APT index and install Python/pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install pytest for the autograder
RUN pip3 install --no-cache-dir pytest

# Create an unprivileged user called "user" with its home directory
RUN useradd -m -s /bin/bash user

# Set up the required directory tree and initial raw log files
RUN mkdir -p /home/user/incidents/raw/INC123 && \
    mkdir -p /home/user/archives && \
    mkdir -p /home/user/incidents/triage

# app.log (90 bytes, two lines, LF-terminated)
RUN printf "2023-11-12 10:00:00 INFO Application started\n2023-11-12 10:05:00 INFO Application stopped\n" \
    > /home/user/incidents/raw/INC123/app.log

# error.log (58 bytes, *intentional* typo "NullPointerExceptio" per tests)
RUN printf "2023-11-12 10:03:00 ERROR NullPointerExceptio encountered\n" \
    > /home/user/incidents/raw/INC123/error.log

# debug.tmp (30 bytes)
RUN printf "temporary file to be excluded\n" \
    > /home/user/incidents/raw/INC123/debug.tmp

# Permissions: directories 0755, files 0644, owned by user:user
RUN chown -R user:user /home/user && \
    find /home/user -type d -exec chmod 755 {} \; && \
    find /home/user -type f -exec chmod 644 {} \;

# Environment variables
ENV LC_ALL=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["bash", "-c", "echo 'Container for INC123 incident task.  Use bash to explore.' && exec /bin/bash"]