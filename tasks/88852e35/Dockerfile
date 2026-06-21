FROM ubuntu:22.04

# Labels
LABEL Author="Container Prep Script"
LABEL Description="Initial state container for the e-commerce transactions processing task"

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/raw

RUN cat >/home/user/project/raw/api_responses.json <<'EOF'
[
  {"id":1,"user":"alice","amount":120.50,"status":"completed","timestamp":"2023-01-15T10:25:00Z"},
  {"id":2,"user":"bob","amount":200.00,"status":"refunded","timestamp":"2023-02-20T13:40:00Z"},
  {"id":3,"user":"carol","amount":75.25,"status":"completed","timestamp":"2022-11-05T09:10:00Z"},
  {"id":4,"user":"dave","amount":300.10,"status":"completed","timestamp":"2023-03-12T16:55:00Z"},
  {"id":5,"user":"erin","amount":50.00,"status":"pending","timestamp":"2023-03-30T08:30:00Z"},
  {"id":6,"user":"frank","amount":180.75,"status":"completed","timestamp":"2022-12-22T19:00:00Z"},
  {"id":7,"user":"grace","amount":215.40,"status":"completed","timestamp":"2023-04-18T11:45:00Z"},
  {"id":8,"user":"heidi","amount":90.00,"status":"refunded","timestamp":"2023-04-20T12:15:00Z"}
]
EOF

RUN chmod 755 /home/user /home/user/project /home/user/project/raw && \
    chmod 644 /home/user/project/raw/api_responses.json