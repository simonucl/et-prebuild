FROM ubuntu:22.04

# From %post
RUN set -e && \
    echo "Updating apt and installing required packages..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq && \
    pip3 --no-cache-dir install pytest && \
    echo "Creating initial project structure..." && \
    mkdir -p /home/user/projects/react-auth/src

RUN cat > /home/user/projects/react-auth/package.json <<'EOF'
{"name":"react-auth","version":"0.1.0","private":true,"dependencies":{"react":"^18.2.0","react-dom":"^18.2.0"},"devDependencies":{"env-cmd":"^10.1.0","react-scripts":"5.0.1"},"scripts":{"test":"echo \"Error: no test specified\" && exit 1"}}
EOF

RUN chmod -R a+rwX /home/user/projects && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# From %environment
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:$PATH"

# From %help (none provided)

# From %runscript
CMD ["bash"]