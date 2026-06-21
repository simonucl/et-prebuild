FROM ubuntu:22.04

# Install Python and pytest (needed by the autograder)
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the task
RUN mkdir -p /home/user/support/diagnostics && \
    chmod -R 777 /home/user

# Create the initial logs.csv with exact required contents
RUN cat > /home/user/support/diagnostics/logs.csv <<'EOF'
timestamp,service,status,message
2023-06-12T10:15:00Z,auth,OK,User login successful
2023-06-12T10:16:12Z,db,ERROR,Connection timeout
2023-06-12T10:17:43Z,auth,ERROR,Invalid credentials
2023-06-12T10:18:07Z,web,OK,Page served
2023-06-12T10:19:22Z,cache,OK,Cache refreshed
2023-06-12T10:20:55Z,db,ERROR,Deadlock detected
2023-06-12T10:21:30Z,web,OK,Page served
2023-06-12T10:22:18Z,auth,OK,Password reset requested
EOF

RUN chmod 644 /home/user/support/diagnostics/logs.csv

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user