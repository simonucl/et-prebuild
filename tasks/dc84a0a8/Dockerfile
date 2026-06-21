FROM ubuntu:22.04

# Update package lists and install Python tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the future test suite
RUN pip3 install --no-cache-dir pytest

# -----------------------------------------------------------------------------
# Prepare initial filesystem state for the IT-support ticket exercise
# -----------------------------------------------------------------------------
# Create the required directory hierarchy
RUN mkdir -p /home/user/support/tickets/open/12345 && \
    mkdir -p /home/user/support/tickets/resolved

# Create the description file with the exact expected contents
RUN printf 'User cannot connect to VPN\n' > /home/user/support/tickets/open/12345/description.txt

# Ensure directories and files are readable and writable by any unprivileged user
RUN chmod -R a+rX /home/user/support && \
    chmod a+rw /home/user/support/tickets/open/12345/description.txt

# Set permissions on home directory
RUN chmod 755 /home/user

# Labels
LABEL Author="Task preparation by Apptainer AI assistant"
LABEL Description="Container pre-configured with ticket directory structure and pytest for automated testing."