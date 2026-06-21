FROM ubuntu:22.04

# Labels
LABEL Author="devsecops-template"
LABEL Description="Container for DevSecOps CSV-to-JSON exercise with pytest installed"

# Update package lists and install required utilities
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        jq \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/devsecops/policy_input && \
    mkdir -p /home/user/devsecops/policy_output && \
    mkdir -p /home/user/devsecops/logs

# Create the CSV input file with exact required contents
RUN cat > /home/user/devsecops/policy_input/services.csv <<'EOF'
service,port,protocol,approved
ssh,22,tcp,yes
http,80,tcp,yes
telnet,23,tcp,no
smtp,25,tcp,yes
ftp,21,tcp,no
EOF

# Make everything under /home/user/devsecops writable
RUN chmod -R 0777 /home/user/devsecops && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user

CMD ["bash", "-c", "echo 'DevSecOps exercise container.' && echo 'Run your commands inside this shell or exec directly.' && /bin/bash"]