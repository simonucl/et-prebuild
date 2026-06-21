FROM ubuntu:22.04

# Base tools
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates tzdata && \
    pip3 install --no-cache-dir pytest

# Directory layout
RUN mkdir -p /home/user/incidents/daily-20240201 && \
    mkdir -p /home/user/incidents/daily-20240205 && \
    mkdir -p /home/user/incidents/daily-20240310 && \
    mkdir -p /home/user/incidents/daily-20240312

# Populate log contents - daily-20240201/system.log
RUN cat <<'EOF' > /home/user/incidents/daily-20240201/system.log
2024-02-01 12:34:56 INFO:  Service started
2024-02-01 12:35:01 ERROR: CODE1001 Unable to connect to database
2024-02-01 12:36:00 WARN:  Low memory
2024-02-01 12:37:22 ERROR: CODE1002 Timeout while reading response
EOF

# Populate log contents - daily-20240205/app.log
RUN cat <<'EOF' > /home/user/incidents/daily-20240205/app.log
2024-02-05 09:10:11 ERROR: CODE1002 Timeout while reading response
2024-02-05 09:15:00 INFO:  User logged in
2024-02-05 09:16:45 ERROR: CODE1003 Null pointer exception
EOF

# Populate log contents - daily-20240310/system.log
RUN cat <<'EOF' > /home/user/incidents/daily-20240310/system.log
2024-03-10 10:00:00 ERROR: CODE1004 Disk full
2024-03-10 10:05:00 INFO:  cleanup done
EOF

# Populate log contents - daily-20240312/app.log
RUN cat <<'EOF' > /home/user/incidents/daily-20240312/app.log
2024-03-12 11:00:00 ERROR: CODE1002 Timeout while reading response
2024-03-12 11:01:00 ERROR: CODE1001 Unable to connect to database
EOF

# Set precise modification times
# Cold logs – strictly before 2024-03-01 00:00:00 UTC
RUN touch -d "2024-02-01 12:38:00 UTC" /home/user/incidents/daily-20240201/system.log && \
    touch -d "2024-02-05 09:17:00 UTC" /home/user/incidents/daily-20240205/app.log

# Hot logs – on/after 2024-03-01 00:00:00 UTC
RUN touch -d "2024-03-10 10:06:00 UTC" /home/user/incidents/daily-20240310/system.log && \
    touch -d "2024-03-12 11:02:00 UTC" /home/user/incidents/daily-20240312/app.log

# Permissions
# The student (non-root runtime user) must be able to move / create / delete
# within /home/user, so make it world-writable inside the image.
RUN chmod -R 0777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

CMD ["echo", "Container for 'Incident Triage' exercise. Run your shell commands to complete the task."]