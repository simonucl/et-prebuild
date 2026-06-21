FROM ubuntu:22.04

# Update package index and install Python 3 and pip
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip

# Install pytest for the grading tests
RUN pip3 install --no-cache-dir pytest

# Create the /home/user hierarchy
RUN mkdir -p /home/user/security

# Ensure write permissions for all users
RUN chmod 0777 /home/user/security

# Create the initial limits.csv file
RUN cat >/home/user/security/limits.csv <<'EOF'
Parameter,Current
nofile,4096
nproc,8192
memlock,16384
fsize,1048576
EOF

# Apply environment-time permissions
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONIOENCODING=utf-8

# Runscript equivalent
CMD echo "Container for the 'optimize_limits' exercise." && \
    echo "You can run: python3 /home/user/security/optimize_limits.py" && \
    echo "or start a shell to work on the task."