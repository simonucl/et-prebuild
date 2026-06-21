FROM ubuntu:22.04

# Labels
LABEL Author="NetworkLogsFixture"
LABEL Description="Container supplying initial network traceroute log fixture and pytest for grading."

ENV DEBIAN_FRONTEND=noninteractive

# --------------------------------------------------------------------- #
# Fundamental system packages and Python tooling
# --------------------------------------------------------------------- #
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip install --no-cache-dir pytest

# --------------------------------------------------------------------- #
# Prepare fixture directory tree and files under /home/user
# --------------------------------------------------------------------- #
RUN mkdir -p /home/user/network_logs/region1 && \
    mkdir -p /home/user/network_logs/region2/backup

# region1/router1.trace
RUN cat > /home/user/network_logs/region1/router1.trace << 'EOF'
PING 10.0.0.1
success
timeout
timeout
timeout
end
EOF

# region1/router2.trace
RUN cat > /home/user/network_logs/region1/router2.trace << 'EOF'
PING 10.0.0.2
success
end
EOF

# region2/router3.trace
RUN cat > /home/user/network_logs/region2/router3.trace << 'EOF'
TRACE 10.1.0.1
timeout
ok
timeout
end
EOF

# region2/backup/router4.trace
RUN cat > /home/user/network_logs/region2/backup/router4.trace << 'EOF'
PROBE 10.2.0.1
timeout
timeout
timeout
timeout
timeout
done
EOF

# --------------------------------------------------------------------- #
# Permissions
#   • Directories: 755 (rwxr-xr-x)
#   • .trace files: 666 (rw-rw-rw-) so the non-root test user can edit
# --------------------------------------------------------------------- #
RUN find /home/user/network_logs -type d -exec chmod 755 {} \; && \
    find /home/user/network_logs -type f -name "*.trace" -exec chmod 666 {} \; && \
    chmod 755 /home/user

WORKDIR /home/user

CMD ["/bin/bash"]