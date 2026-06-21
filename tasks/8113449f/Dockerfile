FROM ubuntu:22.04

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user and home directory
RUN useradd -m -s /bin/bash user

# Create the required directory structure
RUN mkdir -p /home/user/storage_reports && \
    chmod 777 /home/user/storage_reports

# Create seed file
RUN cat <<'EOF' >/home/user/storage_reports/current_usage.csv
filesystem,used_GB,available_GB
/,12,38
/home,40,60
/var/log,4,6
/tmp,1,9
EOF

RUN chmod 644 /home/user/storage_reports/current_usage.csv && \
    chmod 755 /home/user && \
    chown -R user:user /home/user

# Set environment variables
ENV LC_ALL=C
ENV LANG=C
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Labels
LABEL Author="user"
LABEL Description="Initial state for storage usage percentage task with pytest installed"

USER user
WORKDIR /home/user