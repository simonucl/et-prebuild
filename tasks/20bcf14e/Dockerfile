FROM ubuntu:22.04

# Labels
LABEL Author="incident-response-task"
LABEL Description="Base image for DNS-resolution IR exercise"

# Update package lists and install Python and build essentials
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    # Install pytest for the assessment harness
    pip3 install --no-cache-dir pytest && \
    # Create the regular, non-privileged user expected by the tests
    useradd -m -s /bin/bash user && \
    # Ensure the home directory has safe default permissions
    chmod 0755 /home/user && \
    chown -R user:user /home/user && \
    # Clean up to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# NOTE:
# - We deliberately DO NOT create /home/user/ir or the dns_resolution.log
#   file; those are to be created by the student during the exercise.
# - No changes are made that would allow "metadata.google.internal" or
#   "definitely-not-real.tld" to resolve, which aligns with the test
#   expectations.

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Default entrypoint: drop into a shell for interactive work
CMD ["/bin/bash"]