FROM ubuntu:22.04

# System packages and Python tooling
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state expected by the exercise
RUN mkdir -p /home/user/source_logs

# app_server.log
RUN cat > /home/user/source_logs/app_server.log <<'EOF'
2023-03-01 12:00:00 INFO Server started
2023-03-01 12:05:00 ERROR Failed to connect to DB
2023-03-01 12:10:00 INFO Retrying...
2023-03-01 12:10:05 ERROR Retry failed
2023-03-01 12:10:10 INFO Giving up
2023-03-01 13:00:00 INFO Daily job executed
2023-03-01 13:15:00 ERROR Daily job failed
2023-03-01 13:16:00 INFO Notifying admin
EOF

# app_worker.log
RUN cat > /home/user/source_logs/app_worker.log <<'EOF'
2023-03-02 08:00:00 INFO Worker started
2023-03-02 08:01:00 INFO Processing message 1
2023-03-02 08:01:10 ERROR Message 1 failed
2023-03-02 08:01:20 INFO Message 1 requeued
2023-03-02 08:10:00 INFO Worker idle
EOF

# app_2022_old.log
RUN cat > /home/user/source_logs/app_2022_old.log <<'EOF'
2022-12-31 23:55:00 INFO Shutdown initiated
2022-12-31 23:55:05 INFO Waiting for tasks
2022-12-31 23:55:10 INFO Tasks complete
2022-12-31 23:55:15 INFO Shutdown complete
EOF

# system.log
RUN cat > /home/user/source_logs/system.log <<'EOF'
2023-03-03 09:00:00 INFO System check start
2023-03-03 09:00:10 WARN CPU usage high
2023-03-03 09:00:20 ERROR Fan failure
2023-03-03 09:00:30 INFO Fan restart attempt
2023-03-03 09:00:40 ERROR Fan restart failed
2023-03-03 09:00:50 INFO Alarm triggered
2023-03-03 09:01:00 INFO Cooling system engaged
2023-03-03 09:01:10 INFO Logging event
2023-03-03 09:01:20 INFO Event logged
2023-03-03 09:01:30 INFO System check end
EOF

# readme.txt
RUN cat > /home/user/source_logs/readme.txt <<'EOF'
These are demonstration logs used by the training task.
EOF

# Permissions
RUN chmod -R a+r /home/user/source_logs && \
    chmod a+rwxt /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user

CMD ["/bin/bash", "-c", "echo 'This container provides the initial state for the log-processing exercise.' && echo 'To start working, open a shell:' && echo '  docker exec -it <container> /bin/bash'"]