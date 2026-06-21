FROM ubuntu:22.04

# Help:
# This container provides the initial filesystem layout for the
# “SQLite catalogue” exercise. It already contains the tiny project
# located at /home/user/my_project with three files whose exact byte
# sizes are required by the automated grading suite. Python (with
# pytest) and the sqlite3 CLI tool are pre‑installed so that learners
# can complete the task entirely from the terminal.

LABEL Author="Container builder for SQLite catalogue exercise"

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/home/user

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/my_project && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/my_project

RUN cat >/home/user/my_project/main.py <<'EOF'
print("Hello, World!")
EOF

RUN cat >/home/user/my_project/utils.py <<'EOF'
def add(a, b): return a + b
EOF

RUN cat >/home/user/my_project/README.md <<'EOF'
# My Project
This is a sample project structure.
EOF

RUN chmod 0644 /home/user/my_project/main.py \
               /home/user/my_project/utils.py \
               /home/user/my_project/README.md