FROM ubuntu:22.04

# Labels
LABEL Author="Autograder Setup"
LABEL Description="Container prepared for the uptime monitor SHA-256 verification exercise."

# Basic OS tooling and Python testing framework
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils \
    && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user with home directory /home/user
RUN useradd -m -s /bin/bash user

# Create the required directory structure for the exercise
RUN mkdir -p /home/user/uptime_monitor/reports

# Create the zero-byte report file
RUN touch /home/user/uptime_monitor/reports/uptime_2024-04-25.log

# Create the corresponding SHA-256 manifest (two spaces before the filename)
RUN printf "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  uptime_2024-04-25.log\n" \
    > /home/user/uptime_monitor/reports/uptime_2024-04-25.log.sha256

# Ensure correct ownership and sensible permissions
RUN chown -R user:user /home/user/uptime_monitor && \
    chmod 755 /home/user && \
    chmod -R a+rX,go-w /home/user/uptime_monitor

# Environment variables
ENV PATH="/usr/local/bin:$PATH"