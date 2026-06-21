FROM ubuntu:22.04

# Install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        coreutils

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create non-root user
RUN useradd -m -u 1000 user

# Prepare directory & file structure
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/reports

# Create the backup file containing exactly the ASCII text "hello"
# (five bytes, no trailing newline).
RUN printf 'hello' > /home/user/data/backup.tar.gz

# Set appropriate ownership and permissions
RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data /home/user/reports && \
    chmod 644 /home/user/data/backup.tar.gz

LABEL Author="backup-integrity task setup"

# No changes to $HOME; leave environment untouched.