FROM ubuntu:22.04

# Update APT index and install Python & pip
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Create the /home/user hierarchy
RUN mkdir -p /home/user/build/logs

# Make sure the learner (non-root) can create /home/user/build/reports later
RUN chmod -R 0777 /home/user/build

# Populate the CI log with the exact required contents
RUN cat >/home/user/build/logs/mobile_ci_2023-10-07.log <<'EOF'
[00:01:12] MODULE=app_core PLATFORM=android RESULT=SUCCESS DURATION=120
[00:03:15] MODULE=app_ui PLATFORM=android RESULT=WARNING DURATION=60
[00:04:55] MODULE=networking PLATFORM=ios RESULT=FAILURE DURATION=45
[00:06:01] MODULE=database PLATFORM=android RESULT=SUCCESS DURATION=75
[00:07:40] MODULE=push_service PLATFORM=ios RESULT=FAILURE DURATION=30
[00:08:25] MODULE=analytics PLATFORM=android RESULT=SUCCESS DURATION=90
[00:10:55] MODULE=billing PLATFORM=ios RESULT=SUCCESS DURATION=110
[00:12:05] MODULE=crash_reporter PLATFORM=android RESULT=WARNING DURATION=55
EOF

# Ensure the log file is world-readable
RUN chmod 0644 /home/user/build/logs/mobile_ci_2023-10-07.log

# Set permissions on /home/user
RUN chmod 755 /home/user

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8