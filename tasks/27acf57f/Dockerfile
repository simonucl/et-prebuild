FROM ubuntu:22.04

# Labels
LABEL Author="Container setup generated for experimental log summarisation task"

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Update package index and install Python/pip
RUN set -e && \
    echo "Updating package index and installing Python/pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip

# Install pytest for the evaluation suite
RUN echo "Installing pytest for the evaluation suite..." && \
    pip install --no-cache-dir pytest

# Create base directory structure
RUN echo "Creating base directory structure and log files..." && \
    mkdir -p /home/user/data_runs && \
    chmod 777 /home/user

# Create run1.log
RUN cat > /home/user/data_runs/run1.log << 'EOF'
[2024-01-01 10:00:00] INFO Starting run
[2024-01-01 10:01:00] ERROR Failed to open file
[2024-01-01 10:02:00] WARNING Low memory
[2024-01-01 10:03:00] ERROR Timeout occurred
[2024-01-01 10:04:00] INFO Run finished
EOF

# Create run2.log
RUN cat > /home/user/data_runs/run2.log << 'EOF'
[2024-02-01 11:00:00] INFO Starting run
[2024-02-01 11:15:00] ERROR Invalid parameter
[2024-02-01 11:30:00] INFO Run finished
EOF

# Create run3.log
RUN cat > /home/user/data_runs/run3.log << 'EOF'
[2024-03-05 09:00:00] INFO Starting run
[2024-03-05 09:05:00] WARNING Disk almost full
[2024-03-05 09:10:00] INFO Still running
[2024-03-05 09:15:00] ERROR Segmentation fault
[2024-03-05 09:20:00] ERROR Failed to allocate memory
[2024-03-05 09:25:00] ERROR Unknown exception
[2024-03-05 09:30:00] INFO Run finished
EOF

# Set sensible permissions
RUN chmod 755 /home/user/data_runs && \
    chmod 644 /home/user/data_runs/run*.log && \
    echo "Initial container setup complete."

# Help information (as comment)
# This container image contains the pre-populated log files in
# /home/user/data_runs/ and pytest for automated grading. Students will
# create /home/user/analysis_results/error_summary.csv based on the logs.