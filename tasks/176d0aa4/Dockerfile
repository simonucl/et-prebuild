FROM ubuntu:22.04

# Author: "Container build for SQLite log analysis task"
# Description: "Provides initial data and tools (sqlite3, pytest) for the agent."

ENV PATH="/usr/local/bin:/usr/bin:${PATH}"
ENV LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
        locales && \
    sed -i '/en_US.UTF-8/ s/^# //g' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat <<'CSVEOF' >/home/user/logs/events.csv
timestamp,severity,message
2023-07-10 10:00:00,INFO,Service started
2023-07-10 10:05:00,WARNING,High memory usage
2023-07-10 10:10:00,ERROR,Service crashed
2023-07-10 10:15:00,INFO,Service restarted
2023-07-10 10:20:00,ERROR,Missing config file
2023-07-10 10:25:00,WARNING,Disk near capacity
2023-07-10 10:30:00,INFO,Health check ok
2023-07-10 10:35:00,ERROR,Service crashed
CSVEOF

RUN chmod 755 /home /home/user /home/user/logs && \
    chmod 644 /home/user/logs/events.csv && \
    chmod 755 /home/user