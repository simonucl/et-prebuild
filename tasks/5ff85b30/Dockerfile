FROM ubuntu:22.04

# Labels
LABEL Author="agent-prep"
LABEL Description="Sets up initial IR exercise state and installs pytest."

# --------------------------------------------------------------------- #
# Basic tooling                                                         #
# --------------------------------------------------------------------- #
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    pip3 install --no-cache-dir pytest

# --------------------------------------------------------------------- #
# Create the initial investigation directory tree                       #
# --------------------------------------------------------------------- #
RUN set -e && \
    BASE_DIR="/home/user/investigation" && \
    UPLOADS_DIR="${BASE_DIR}/uploads" && \
    REF_DIR="${BASE_DIR}/reference" && \
    mkdir -p "${UPLOADS_DIR}" && \
    mkdir -p "${REF_DIR}" && \
    chmod -R a+rwX /home/user

# --------------------------------------------------------------------- #
# Populate uploads/ with the files mentioned in the task description    #
# --------------------------------------------------------------------- #
# 1. safe.txt  (contains "hello" without a trailing newline)
RUN printf 'hello' > /home/user/investigation/uploads/safe.txt

# 2. malicious.bin (zero-byte file)
RUN : > /home/user/investigation/uploads/malicious.bin

# 3. unknown.dat (contains "test" without a trailing newline)
RUN printf 'test' > /home/user/investigation/uploads/unknown.dat

# --------------------------------------------------------------------- #
# Populate reference hash databases                                     #
# --------------------------------------------------------------------- #
RUN echo '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824' \
    > /home/user/investigation/reference/known_safe_hashes.txt

RUN echo 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' \
    > /home/user/investigation/reference/known_malware_hashes.txt

# --------------------------------------------------------------------- #
# Clean up                                                              #
# --------------------------------------------------------------------- #
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------- #
# Environment                                                           #
# --------------------------------------------------------------------- #
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Set permissions on home directory
RUN chmod 755 /home/user

# Default command
CMD ["echo", "Container built for the IR hashing exercise."]