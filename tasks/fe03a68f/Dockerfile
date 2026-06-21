FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial directory & data structure for the exercise
RUN mkdir -p /home/user/data_experiments/dataset_A && \
    mkdir -p /home/user/data_experiments/dataset_B && \
    mkdir -p /home/user/output && \
    chmod 0777 /home/user/output

# Populate dataset_A CSV files
RUN cat > /home/user/data_experiments/dataset_A/file1.csv <<'EOF'
id,value
1,2.5
2,3.1
EOF

RUN cat > /home/user/data_experiments/dataset_A/file2.csv <<'EOF'
id,value
1,7.2
2,5.4
3,6.0
EOF

# Populate dataset_B CSV file
RUN cat > /home/user/data_experiments/dataset_B/measurements.csv <<'EOF'
time,reading
00:00,0.12
01:00,0.11
02:00,0.15
03:00,0.10
EOF

# Read & execute permissions for datasets
RUN chmod -R 0755 /home/user/data_experiments && \
    chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8