FROM ubuntu:22.04

# Author AI_Apptainer_Assistant
# Description "Base image for capacity-planning task. Provides Python, pytest and standard system tools."

# This Apptainer image contains:
#   • Python 3
#   • pytest
#   • Standard Linux monitoring utilities (procps)
# A writable /home/user directory has been created so that learners can
# generate /home/user/capacity_planning/report.log during the exercise.

RUN set -e && \
    echo "Updating package lists..." && \
    apt-get update -y && \
    echo "Installing required packages..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        procps && \
    echo "Installing pytest..." && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating writable /home/user directory for the exercise..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Python and pip are easily accessible
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user

CMD ["echo", "Container for capacity-planning exercise. Invoke your commands or tests as needed."]