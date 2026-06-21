FROM ubuntu:22.04

# Help/label metadata
LABEL Author="Auto-generated container for optimisation-solver curation task"

# Update APT and install Python + pip + pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare staging area
RUN mkdir -p /home/user/curation/binaries

# Create placeholder archives
RUN printf 'CBC binary placeholder v2.10.5\n'  > /home/user/curation/binaries/cbc-2.10.5-linux-x86_64.tar.gz
RUN printf 'GLPK binary placeholder v5.0\n'    > /home/user/curation/binaries/glpk-5.0-linux-x86_64.tar.gz
RUN printf 'SCIP binary placeholder v8.0.3\n'  > /home/user/curation/binaries/scip-8.0.3-linux-x86_64.tar.gz

# Permissions
RUN chmod 755 /home /home/user /home/user/curation /home/user/curation/binaries && \
    chmod 644 /home/user/curation/binaries/*.tar.gz