FROM ubuntu:22.04

# Labels
LABEL Author="permission-audit-setup"

# Help information (as comments)
# This container image provides the initial filesystem state for the
# "permission audit" exercise.  The workspace directory
#     /home/user/audit_workspace
# contains a static snapshot file named
#     system_file_listing.txt
# which the learner will parse with awk/sed to generate the required
# audit report.  Pytest is pre-installed so that the supplied test
# suite can verify the environment.

# Update package list and install required tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gawk \
        sed \
        ca-certificates

# Install pytest for the validation suite
RUN pip3 install --no-cache-dir pytest

# Prepare initial workspace and input snapshot
# Ensure the /home/user hierarchy exists and is writable
RUN mkdir -p /home/user/audit_workspace && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/audit_workspace

# Create the static "ls -l" snapshot file with exactly eight lines
RUN cat << 'EOF' > /home/user/audit_workspace/system_file_listing.txt
-rwxrwsr-x 1 root developers 1234 Jan  3 12:34 /usr/local/bin/devtool
-rw-rw-r-- 1 user user 234 Jan 2 12:00 /home/user/doc.txt
-rw-r--r-- 1 root root 1234 Jan 3 12:34 /etc/passwd
-rwsr-xr-x 1 root root 14256 Jan 1 10:00 /usr/bin/su
drwxrwxrwt 15 root root 4096 Jan 4 08:20 /tmp
-rw-rw-rw- 1 www-data www-data 1024 Jan 5 09:10 /var/www/html/index.php
-rwxr-sr-x 1 root staff 2048 Jan 6 11:11 /usr/local/bin/gidtool
-rw------- 1 user user 512 Jan 2 15:00 /home/user/.ssh/id_rsa
EOF

# Make the snapshot file world-readable
RUN chmod 0644 /home/user/audit_workspace/system_file_listing.txt

# Environment variables
ENV LC_ALL=C.UTF-8

# Set working directory
WORKDIR /home/user