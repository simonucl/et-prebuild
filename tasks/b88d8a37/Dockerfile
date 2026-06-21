FROM ubuntu:22.04

# Labels
LABEL Author="apptainer-task-prep"
LABEL Description="Initial state for SSH key-pair + CSV aggregation task"

# Post installation
RUN set -e && \
    echo "Updating apt repositories and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        openssh-client \
        python3 \
        python3-pip && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating user 'user' with home directory /home/user ..." && \
    useradd -m -s /bin/bash user && \
    echo "Setting up directory structure..." && \
    install -d -m 0700  /home/user/.ssh && \
    install -d -m 0755  /home/user/datasets && \
    install -d -m 0755  /home/user/outputs && \
    install -d -m 0700  /home/user/server_access

# Create sales_q1.csv
RUN cat > /home/user/datasets/sales_q1.csv <<'EOF'
Category,Revenue
A,100
B,150
C,200
EOF

# Create sales_q2.csv
RUN cat > /home/user/datasets/sales_q2.csv <<'EOF'
Category,Revenue
A,120
B,130
D,90
EOF

# Set permissions for CSV files
RUN chmod 0644 /home/user/datasets/sales_q1.csv /home/user/datasets/sales_q2.csv

# Create authorized_keys_data with dummy key
RUN cat > /home/user/server_access/authorized_keys_data <<'EOF'
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJdummYPvOjJk9pc6V5u5W0bkxz0eG4DLXo8boxexisting existing_key
EOF

# Set permissions for authorized_keys_data
RUN chmod 0600 /home/user/server_access/authorized_keys_data

# Ensure correct ownership
RUN chown -R user:user /home/user

# Set home directory permissions
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD ["bash", "-c", "echo 'Container for data-pipeline task. Drop into a shell with: docker exec -it <container> bash'"]