FROM ubuntu:22.04

# Author "ChatGPT"
# Description "Initial container setup for help-desk ticket #551 task with pytest installed."

RUN set -e \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/mock_logs \
 && chmod 777 /home/user \
 && chmod 755 /home/user/mock_logs

RUN cat > /home/user/mock_logs/auth.log <<'EOF'
Jun  1 08:14:52 localhost sshd[1245]: Failed password for invalid user admin from 10.0.0.15 port 42422 ssh2
Jun  1 08:14:55 localhost sshd[1245]: Connection closed by 10.0.0.15 port 42422 [preauth]
Jun  1 08:15:02 localhost sshd[1247]: Failed password for root from 10.0.0.15 port 42423 ssh2
Jun  1 08:15:04 localhost sshd[1247]: Connection closed by 10.0.0.15 port 42423 [preauth]
Jun  1 08:16:27 localhost sshd[1251]: Accepted password for john from 10.0.0.16 port 42424 ssh2
Jun  1 08:16:30 localhost sshd[1251]: Failed password for user john from 10.0.0.16 port 42424 ssh2
EOF

RUN chmod 644 /home/user/mock_logs/auth.log