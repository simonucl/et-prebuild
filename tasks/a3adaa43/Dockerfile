FROM ubuntu:22.04

# Prepare environment
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest

# Create directory tree
RUN mkdir -p /home/user/data

# Create access-log.html
RUN cat <<'HTML_EOF' >/home/user/data/access-log.html
<!DOCTYPE html>
<html>
<head><title>login log</title></head>
<body>
<pre id="log">
2024-05-05 10:01:22 - LOGIN - user:alice  - status:SUCCESS
2024-05-05 10:02:47 - LOGIN - user:bob    - status:FAIL
2024-05-05 10:03:19 - LOGIN - user:dave   - status:SUCCESS
2024-05-05 10:05:12 - LOGIN - user:carol  - status:FAIL
2024-05-05 10:06:54 - LOGIN - user:erin   - status:SUCCESS
</pre>
</body>
</html>
HTML_EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/access-log.html

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

LABEL Author="Container Build Automation"
LABEL Description="Environment for log-analysis CLI exercise with pytest pre-installed"