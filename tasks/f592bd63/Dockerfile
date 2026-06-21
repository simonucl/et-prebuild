FROM ubuntu:22.04

# Author "Automation Specialist"

# This container sets up the starting environment for the regular‑expression
# log‑filtering exercise.
# It provides:
#   - /home/user/logs/app.log with predefined content
#   - pytest installed for automated grading

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs

RUN cat <<'EOF' > /home/user/logs/app.log
2021-09-14 10:12:01,234 INFO  [module]  - Started
2021-09-15 11:01:17,890 ERROR [auth]    - Invalid credentials
2021-09-15 11:02:00,123 WARN  [auth]    - Slow response
2021-09-15 11:05:43,456 ERROR [auth]    - User locked out
2021-09-16 09:15:00,001 ERROR [db]      - Connection lost
2021-09-15 12:00:00,000 INFO  [module]  - Ended
2021-09-15 13:15:10,678 ERROR [payment] - Payment failed
2021-09-15 14:20:30,789 DEBUG [payment] - Debug message
2021-09-14 15:10:50,987 ERROR [module]  - Unexpected error
EOF

RUN chmod 644 /home/user/logs/app.log

ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"