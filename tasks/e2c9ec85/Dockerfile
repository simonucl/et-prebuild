FROM ubuntu:22.04

# Update apt index and install Python with pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Create the reports directory with broad write permissions
RUN mkdir -p /home/user/build_reports && \
    chmod 0777 /home/user/build_reports

# Populate the build log with the exact required contents
RUN cat > /home/user/build_reports/build_full_2023-09-15.log << 'EOF'
ID;Platform;Start;End;Status;Duration(s)
B1021;android;2023-09-15T01:02:03Z;2023-09-15T01:07:10Z;Success;307
B1022;ios;2023-09-15T02:10:00Z;2023-09-15T02:24:45Z;Failed;885
B1023;android;2023-09-15T03:05:30Z;2023-09-15T03:11:01Z;Success;331
B1024;ios;2023-09-15T04:20:10Z;2023-09-15T04:25:35Z;Success;325
EOF

RUN chmod 0644 /home/user/build_reports/build_full_2023-09-15.log

# Set permissions on home directory
RUN chmod 755 /home/user

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8