FROM ubuntu:22.04

# Labels
LABEL Author="checksum-frequency-task"
LABEL Description="Container prepared for the checksum frequency Apptainer assignment"

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create the home path and data directory expected by the tests.
RUN mkdir -p /home/user/data

# Make sure the future, non-root runtime user has write permission.
RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/data

# Create the raw checksum list exactly as specified (12 lines, each
# terminated by a single UNIX newline).
RUN cat > /home/user/data/daily_checksums.txt << 'EOF'
a1b2c3d4e5f6g7h8i9j0
11111111111111111111
a1b2c3d4e5f6g7h8i9j0
22222222222222222222
33333333333333333333
11111111111111111111
22222222222222222222
22222222222222222222
44444444444444444444
a1b2c3d4e5f6g7h8i9j0
55555555555555555555
11111111111111111111
EOF

# Ensure correct permissions on the file (readable by all, immutable
# content before the student modifies anything else).
RUN chmod 0644 /home/user/data/daily_checksums.txt

# Guarantee that the target output file does NOT yet exist.
RUN rm -f /home/user/data/checksum_frequency.log

# Environment variables
ENV LC_ALL=C
ENV LANG=C
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user