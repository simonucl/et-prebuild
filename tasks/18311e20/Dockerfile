FROM ubuntu:22.04

# Labels
LABEL Author="your_name"
LABEL Description="Container for firewall-configuration task (clean initial state)."

# Post installation
RUN set -e && \
    echo "Updating apt repositories and installing required packages..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        git \
        bash && \
    echo "Adding non-root user 'user' with home directory /home/user ..." && \
    adduser --disabled-password --gecos "" user && \
    chown -R user:user /home/user && \
    echo "Installing pytest for the autograder ..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set permissions on /home/user
RUN chmod 755 /home/user

# Help information (as comments)
# This container is prepared for the firewall-configuration coding task.
# The initial filesystem state is intentionally clean:
#   • /home/user/ci does not exist.
#   • No firewall scripts or logs are present.
# Students will author these as part of their solution.

# Default command
CMD ["/bin/bash", "-l"]