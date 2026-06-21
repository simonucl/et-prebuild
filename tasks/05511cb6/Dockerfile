FROM ubuntu:22.04

# %post
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gawk \
        sed && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/incident_logs

RUN cat >/home/user/incident_logs/app_2023-07-15.log <<'EOF'
2023-07-15 10:12:05,123 [auth] INFO User john@example.com logged in
2023-07-15 10:13:07,456 [payment] ERROR Failed payment for user jane.doe@example.com: insufficient funds
2023-07-15 10:15:00,789 [search] WARN Slow query
2023-07-15 10:16:12,321 [payment] ERROR Timeout contacting bank API
2023-07-15 10:18:45,654 [auth] ERROR Invalid password for user admin@example.com
2023-07-15 10:20:11,987 [inventory] INFO Stock updated
EOF

RUN cat >/home/user/incident_logs/app_2023-07-16.log <<'EOF'
2023-07-16 09:01:02,111 [auth] INFO User alice@example.com logged in
2023-07-16 09:05:33,222 [search] ERROR Null pointer in search index
2023-07-16 09:10:44,333 [payment] ERROR Currency conversion failed for user bob@example.com
2023-07-16 09:15:55,444 [auth] WARN Token nearing expiry
2023-07-16 09:20:06,555 [payment] ERROR Duplicate transaction detected
2023-07-16 09:25:17,666 [search] ERROR Failed to parse query "foo bar"
EOF

RUN chmod -R 0777 /home/user

# %environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8