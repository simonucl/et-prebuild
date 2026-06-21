FROM ubuntu:22.04

# Labels
LABEL Author="timezone-locale-setup"
LABEL Description="Starter container for the locale/time-zone configuration exercise"

# Basic tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip

# Python test framework
RUN pip3 install --no-cache-dir pytest

# Exercise workspace skeleton
RUN mkdir -p /home/user/observability && \
    chmod -R 0777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"