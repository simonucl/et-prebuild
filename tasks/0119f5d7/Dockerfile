FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    python3 \
    python3-pip \
    ca-certificates

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create a writable home directory for the student
RUN mkdir -p /home/user && chmod 0777 /home/user

# Create entrypoint script to replicate %runscript behavior
RUN cat <<EOF > /entrypoint.sh
#!/bin/bash
chmod 755 /home/user
exec "\$@"
EOF

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]