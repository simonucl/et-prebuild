# Converted from Apptainer .def
FROM ubuntu:22.04

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-client \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        hostname \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python packages
RUN pip3 install --no-cache-dir pytest

# Create non-privileged workspace
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Add passwd/group entry for UID 1000 if missing
RUN if ! getent passwd 1000 >/dev/null 2>&1; then \
        echo "user:x:1000:1000::/home/user:/bin/bash" >> /etc/passwd && \
        echo "user:x:1000:" >> /etc/group ; \
    fi

# Match runscript behavior: ensure directory perms
RUN chmod 755 /home/user

# Default shell entry
CMD ["/bin/bash"]