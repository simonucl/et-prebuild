FROM ubuntu:22.04

# Help / labels from %help and %labels
LABEL Author="Autograder Provisioning"
LABEL Description="Environment for FAILED LOGIN incident-response exercise."
LABEL Version="1.0"

# Environment section (none required)

# Install Python, pytest, and utilities
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip gzip coreutils && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/incidents/syslog-backups && \
    mkdir -p /home/user/scripts && \
    chmod 0777 /home/user/scripts

# Create evidence gzip files
RUN set -e; \
    create_gz() { \
        outfile="$1"; shift; \
        tmpfile="$(mktemp)"; \
        printf "%s\n" "$@" > "$tmpfile"; \
        chmod 755 /home/user; \
        gzip -c "$tmpfile" > "$outfile"; \
        rm -f "$tmpfile"; \
        chmod 0444 "$outfile"; \
    }; \
    create_gz /home/user/incidents/syslog-backups/syslog-2023-07-20.gz \
        "2023-07-20T23:50:00Z auth SSHD[1111]: FAILED LOGIN from 172.16.5.22 port 52000" \
        "2023-07-20T23:51:00Z auth SSHD[1112]: FAILED LOGIN from 10.0.0.5 port 52001" \
        "2023-07-20T23:52:00Z auth SSHD[1113]: FAILED LOGIN from 10.0.0.5 port 52002" ; \
    create_gz /home/user/incidents/syslog-backups/syslog-2023-07-21.gz \
        "2023-07-21T02:13:45Z auth SSHD[1234]: FAILED LOGIN from 192.168.0.101 port 54022" \
        "2023-07-21T03:11:01Z auth SSHD[5678]: FAILED LOGIN from 10.0.0.5 port 49999" \
        "2023-07-21T03:15:32Z auth SSHD[9101]: FAILED LOGIN from 192.168.0.101 port 54025" \
        "2023-07-21T04:00:00Z auth SSHD[9102]: FAILED LOGIN from 192.168.0.101 port 54026" ; \
    create_gz /home/user/incidents/syslog-backups/syslog-2023-07-22.gz \
        "2023-07-22T00:01:12Z auth SSHD[2222]: FAILED LOGIN from 192.168.0.101 port 54030" \
        "2023-07-22T00:05:00Z auth SSHD[2223]: FAILED LOGIN from 172.16.5.22 port 54031" \
        "2023-07-22T01:15:00Z auth SSHD[2224]: FAILED LOGIN from 10.0.0.5 port 54032" \
        "2023-07-22T02:00:00Z auth SSHD[2225]: FAILED LOGIN from 192.168.0.101 port 54033" ; \
    create_gz /home/user/incidents/syslog-backups/syslog-2023-07-23.gz \
        "2023-07-23T11:11:11Z auth SSHD[3333]: FAILED LOGIN from 192.168.0.101 port 55000" \
        "2023-07-23T12:00:00Z auth SSHD[3334]: FAILED LOGIN from 192.168.0.101 port 55001" \
        "2023-07-23T12:30:00Z auth SSHD[3335]: FAILED LOGIN from 10.0.0.5 port 55002"

# Make evidence read-only
RUN chmod -R a-w /home/user/incidents

# Adjust /home/user permissions
RUN chown -R 0:0 /home/user && \
    chmod 0755 /home/user

# Run script equivalent
CMD echo "Container for the FAILED LOGIN triage exercise." && \
    echo "You are expected to create /home/user/scripts/analyze_failed_logins.sh and run it."