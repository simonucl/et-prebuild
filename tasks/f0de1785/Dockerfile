FROM ubuntu:22.04

# %post
RUN set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/audit/raw && \
    mkdir -p /home/user/audit/reports

RUN cat > /home/user/audit/raw/auth_2024-06-10.log << 'EOF'
2024-06-10T09:15:23Z alice 192.168.1.5 SUCCESS
2024-06-10T09:17:45Z bob 10.0.0.12 FAILURE
2024-06-10T10:01:02Z charlie 172.16.0.3 SUCCESS
2024-06-10T11:20:00Z alice 192.168.1.5 FAILURE
EOF

RUN cat > /home/user/audit/raw/auth_2024-06-11.log << 'EOF'
2024-06-11T08:05:12Z bob 10.0.0.12 SUCCESS
2024-06-11T09:55:30Z dave 203.0.113.45 SUCCESS
2024-06-11T10:00:00Z alice 192.168.1.5 SUCCESS
EOF

RUN cat > /home/user/audit/raw/auth_2024-06-12.log << 'EOF'
2024-06-12T07:45:22Z charlie 172.16.0.3 FAILURE
2024-06-12T08:33:00Z eve 198.51.100.17 SUCCESS
2024-06-12T09:00:00Z alice 192.168.1.5 SUCCESS
EOF

RUN chown -R 1000:1000 /home/user && \
    find /home/user -type d -exec chmod 0755 {} \; && \
    find /home/user -type f -exec chmod 0644 {} \;

# %labels
LABEL Author="audit-task-generator"
LABEL Description="Environment for SSH log compliance-audit exercise with pytest pre-installed."

# %help
# This container provides the starting state for the SSH compliance-audit exercise.
# Raw log files are under /home/user/audit/raw.
# The /home/user/audit/reports directory is empty and writable so you can place the
# required artefacts there (unique_user_ip.tsv and command_log.txt).