FROM ubuntu:22.04

# Help text
# This container provides the initial environment for the “username frequency
# report” task. It includes:
#   - /home/user/data/users.log  – the raw log the student must process
#   - pytest – pre-installed for test execution

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data && \
    chmod 0777 /home/user/data

RUN cat > /home/user/data/users.log <<'EOF'
alice
bob
charlie
alice
bob
alice
dave
eve
bob
charlie
charlie
charlie
frank
grace
heidi
ivan
judy
mallory
oscar
peggy
trent
victor
walter
peggy
trent
trent
trent
mallory
mallory
trent
EOF

RUN chmod 0644 /home/user/data/users.log

# Labels and permissions from %labels section
RUN chmod 755 /home/user
LABEL Author="ChatGPT"
LABEL Description="Starter image for username frequency report task (users.log preset, pytest installed)"