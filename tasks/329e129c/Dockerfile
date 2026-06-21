FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Generator"
LABEL Description="Environment for the CI/CD *.tmp cleanup task with pytest pre-installed."

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="$PATH:/home/user/.local/bin"

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial on-disk state expected by the automated tests
# Directory hierarchy
RUN mkdir -p /home/user/ci_cd/build-artifacts/cache

# Required *.tmp files
RUN echo "temp1"       > /home/user/ci_cd/build-artifacts/temp1.tmp && \
    echo "temp2"       > /home/user/ci_cd/build-artifacts/temp2.tmp && \
    echo "cache build" > /home/user/ci_cd/build-artifacts/cache/build123.tmp && \
    echo "old build"   > /home/user/ci_cd/build-artifacts/cache/old.build.tmp

# Non-tmp artefact that must remain intact after the task
RUN printf '\x42\x49\x4E\x00' > /home/user/ci_cd/build-artifacts/important.bin

# Reasonable permissions (readable by the unprivileged runtime user)
RUN find /home/user/ci_cd -type d -exec chmod 755 {} + && \
    find /home/user/ci_cd -type f -exec chmod 644 {} + && \
    chmod 755 /home/user

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for CI/CD *.tmp cleanup task. Run your commands interactively."]