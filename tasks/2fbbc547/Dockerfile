FROM ubuntu:22.04

# Author "Platform Engineering Demo Container"
LABEL Author="Platform Engineering Demo Container"

RUN set -e && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ca-certificates

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project && chmod 777 /home/user

RUN cat <<'EOF' >/home/user/project/README.md
Demo project for secret scanning.
EOF

RUN cat <<'EOF' >/home/user/project/.env
# Demo environment file
DB_PASSWORD=supersecret
AWS_SECRET_ACCESS_KEY=ABCD1234SECRETTEST
EOF

RUN cat <<'EOF' >/home/user/project/app.py
"""
Minimal application file for the demo project.
"""
def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
EOF

RUN chmod 755 /home/user/project && chmod 644 /home/user/project/*