FROM ubuntu:22.04

# Labels
LABEL Author="platform-engineer-task-setup"
LABEL Description="Container for CI temp cleanup exercise"

# Install Python and pytest
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -s /bin/bash user

# ------------------------------------------------------------------
# Create the CI workspace with the required structure and files
# ------------------------------------------------------------------
ENV CI_ROOT="/home/user/ci_temp"

# Directory tree
RUN mkdir -p "${CI_ROOT}/build1" \
             "${CI_ROOT}/build2" \
             "${CI_ROOT}/build3/nested"

# build1
RUN printf "artifact build 1 – UNSAFE artefact\nUNSAFE\n" > "${CI_ROOT}/build1/artifact1.tmp" && \
    printf "This file should be kept as-is.\n" > "${CI_ROOT}/build1/keep.txt" && \
    printf "Some harmless temporary notes.\n" > "${CI_ROOT}/build1/notes.tmp"

# build2
RUN printf "Debug information containing UNSAFE marker.\nUNSAFE\n" > "${CI_ROOT}/build2/debug.tmp" && \
    printf "Background noise tmp, safe.\n" > "${CI_ROOT}/build2/noise.tmp" && \
    printf "Regular build log.\n" > "${CI_ROOT}/build2/other.log"

# build3 / nested
RUN printf "Nested log file.\n" > "${CI_ROOT}/build3/nested/inner.log" && \
    printf "Nested tmp with UNSAFE token.\nUNSAFE\n" > "${CI_ROOT}/build3/nested/inner.tmp"

# Ensure normal read permissions for all users
RUN chmod -R a+rX /home/user/ci_temp && \
    chown -R user:user /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set home directory permissions at runtime and set working directory
RUN chmod 755 /home/user

WORKDIR /home/user

USER user

CMD echo "This container is prepared for the CI cleanup exercise." && \
    echo "Use 'pytest' to run the pre-configured test suite."