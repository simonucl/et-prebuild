FROM ubuntu:22.04

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Update package index and install Python + pip
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/experiments/run_01

# Create metrics.csv
RUN cat > /home/user/experiments/run_01/metrics.csv << 'EOF'
epoch,loss,accuracy
1,0.80,0.71
2,0.60,0.78
3,0.45,0.82
4,0.40,0.84
5,0.38,0.85
EOF

RUN chmod 644 /home/user/experiments/run_01/metrics.csv

# Create mock_ps.txt
RUN cat > /home/user/mock_ps.txt << 'EOF'
PID USER %CPU %MEM COMMAND
1234 user 12.3 1.1 python
2345 user 2.1 15.2 chrome
3456 user 0.5 10.0 java
4567 user 50.0 0.3 gcc
5678 user 0.7 5.5 node
EOF

RUN chmod 644 /home/user/mock_ps.txt

# Set directory permissions (not world-writable)
RUN chmod 755 /home/user && \
    chmod 755 /home/user/experiments && \
    chmod 755 /home/user/experiments/run_01

# Labels
LABEL Author="Apptainer task scaffold"

# Help information (as comment):
# This container provides the initial filesystem layout and tooling
# (including pytest) required for the "diagnostic bundle" exercise.