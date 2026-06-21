FROM ubuntu:22.04

# Author: example
# Description: Container for utils_workspace disk-usage reporting task
#
# Help:
# This container supplies the predefined workspace and installs pytest so
# that the automated grading system can run its tests.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare workspace expected by the automated tests
RUN mkdir -p /home/user/utils_workspace

# Create script1.sh (36 bytes)
RUN printf '#!/bin/bash\n' > /home/user/utils_workspace/script1.sh && \
    printf 'echo "Utility script 1"\n' >> /home/user/utils_workspace/script1.sh

# Create script2.sh (36 bytes)
RUN printf '#!/bin/bash\n' > /home/user/utils_workspace/script2.sh && \
    printf 'echo "Utility script 2"\n' >> /home/user/utils_workspace/script2.sh

# Create README.md (22 bytes)
RUN printf '# Utilities Workspace\n' > /home/user/utils_workspace/README.md

# Make sure the directory is writable so the student can add files later
RUN chmod 0777 /home/user/utils_workspace && \
    chmod 0644 /home/user/utils_workspace/*.sh /home/user/utils_workspace/README.md && \
    chmod 0777 /home/user