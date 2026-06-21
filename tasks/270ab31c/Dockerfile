FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip curl && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem
RUN mkdir -p /home/user/creds && \
    chmod 0777 /home/user/creds

# Create credential file
RUN printf '{"api_key":"old_key_123","expires":"2023-01-01T00:00:00Z"}' > /home/user/creds/api_creds.json && \
    chmod 0666 /home/user/creds/api_creds.json

# Equivalent of %runscript
CMD sh -c "chmod 755 /home/user && echo 'Apptainer container ready for the API credential rotation exercise.'"