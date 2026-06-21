FROM ubuntu:22.04

# Install Python 3 and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial directory structure and sample log file
RUN mkdir -p /home/user/project/logs

RUN cat > /home/user/project/logs/app.log <<'EOF'
2023-08-01 10:15:20 INFO Starting application
2023-08-01 10:15:21 WARN Low memory
2023-08-01 10:15:22 ERROR Could not connect to database
2023-08-01 10:15:25 INFO Retrying connection
2023-08-01 10:15:30 ERROR Connection timeout
2023-08-01 10:15:45 INFO Shutdown initiated
EOF

RUN chmod -R 0777 /home/user

LABEL Author="QaSetup"