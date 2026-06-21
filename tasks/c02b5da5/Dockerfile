FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer task setup"
LABEL Description="Environment pre-configured for the 'active clients' CSV-to-JSON extraction task."

# Help information (as comments):
# This container image supplies the initial state required for the
# customer-filtering assignment.  It already contains:
#
#   • /home/user/data/clients.csv  (the source data file)
#   • Python 3, pip
#   • pytest (for the autograder)
#   • csvkit & jq (optional tools students may use)
#
# Students will run inside the container without root privileges.

# Set environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Update package list and install system packages
RUN set -e && \
    echo "Updating package list and installing system packages..." && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates

# Install Python packages
RUN echo "Installing Python packages..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest csvkit

# Create directory structure
RUN echo "Creating directory structure and the source CSV file..." && \
    mkdir -p /home/user/data && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data

# Create the source CSV file
RUN cat >/home/user/data/clients.csv <<'EOF'
id,name,email,status
1,John Doe,john@example.com,active
2,Jane Smith,jane@example.com,inactive
3,Bob Lee,bob@example.com,active
4,Alice Kim,alice@example.com,pending
EOF

# Ensure the file ends with a newline and has the correct permissions
RUN echo >> /home/user/data/clients.csv && \
    chmod 644 /home/user/data/clients.csv