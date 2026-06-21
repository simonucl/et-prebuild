FROM ubuntu:22.04

# Update APT metadata and install Python + pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install pytest for the grading suite
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the initial filesystem state expected by the grader
# ------------------------------------------------------------------
# Create the log directory structure
RUN mkdir -p /home/user/logs

# Populate /home/user/logs/incident.log with the exact 10 lines
RUN cat >/home/user/logs/incident.log <<'EOF'
[2023-05-10 10:00:00] OK System started.
[2023-05-10 10:01:02] ERR42 Disk failure.
[2023-05-10 10:02:05] WARN27 High memory usage.
[2023-05-10 10:03:07] ERR42 Disk failure.
[2023-05-10 10:04:10] ERR99 Network unreachable.
[2023-05-10 10:05:12] ERR42 Disk failure.
[2023-05-10 10:06:15] WARN27 High memory usage.
[2023-05-10 10:07:17] ERR99 Network unreachable.
[2023-05-10 10:08:20] INFO11 User login.
[2023-05-10 10:09:22] ERR42 Disk failure.
EOF

# Ensure that regular (non-root) container users can read the log file
# and create the /home/user/diagnostics directory later.
RUN chmod -R 0777 /home/user

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

CMD ["echo", "Container for the 'error-code frequency' task ready. Log file located at /home/user/logs/incident.log. Run your solution inside this container."]