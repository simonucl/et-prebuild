FROM ubuntu:22.04

# Labels
LABEL Author="Artifact-Maintenance Task Setup"
LABEL Description="Base image with initial JAR repository and pytest installed."

# Post installation commands
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial repository layout expected by the test-suite
RUN mkdir -p /home/user/artifacts/stable && \
    mkdir -p /home/user/artifacts/testing

# Create the four JAR files with their exact ASCII payloads
RUN printf 'release build 1.0\n' > /home/user/artifacts/stable/library-1.0.jar && \
    printf 'snapshot build 1.1\n' > /home/user/artifacts/stable/library-1.1-SNAPSHOT.jar && \
    printf 'release build 2.0\n' > /home/user/artifacts/testing/tool-2.0.jar && \
    printf 'snapshot build 2.0\n' > /home/user/artifacts/testing/tool-2.0-SNAPSHOT.jar

# Permissions: make directories writable so the (non-root) student can move files around
RUN chmod 777 /home/user && \
    chmod 777 /home/user/artifacts && \
    chmod 777 /home/user/artifacts/stable && \
    chmod 777 /home/user/artifacts/testing

# Ensure the JAR files are at least readable by everyone
RUN chmod 644 /home/user/artifacts/stable/library-1.0.jar && \
    chmod 644 /home/user/artifacts/stable/library-1.1-SNAPSHOT.jar && \
    chmod 644 /home/user/artifacts/testing/tool-2.0.jar && \
    chmod 644 /home/user/artifacts/testing/tool-2.0-SNAPSHOT.jar

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8