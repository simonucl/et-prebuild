FROM ubuntu:22.04

# Labels
LABEL Author="task-preparation-bot"
LABEL Description="Container for documentation warning extraction task – includes pytest and initial build.log state."

# Post installation
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial workspace expected by the automated tests
RUN mkdir -p /home/user/project/logs

# Create build.log with the exact required contents
RUN cat > /home/user/project/logs/build.log <<'EOF'
2024-04-10 10:15:23 INFO  [INIT] : Starting build
2024-04-10 10:15:25 WARNING [DOC-1001]: Deprecated tag <note> found in file intro.md
2024-04-10 10:15:26 ERROR [DOC-9002]: Missing image intro.png referenced in intro.md
2024-04-10 10:15:27 WARNING [DOC-1002]: Obsolete attribute "align" in file layout.html
2024-04-10 10:15:28 INFO  [CHECK] : Spellcheck completed
2024-04-10 10:15:29 WARNING [DOC-1001]: Deprecated tag <note> found in file usage.md
2024-04-10 10:15:30 WARNING [DOC-1003]: Long line (>120 chars) in getting_started.rst:432
2024-04-10 10:15:31 INFO  [BUILD] : Build step completed
2024-04-10 10:15:32 WARNING [DOC-1002]: Obsolete attribute "align" in file legacy.html
2024-04-10 10:15:33 WARNING [DOC-1004]: Internal link reference missing in api.md
2024-04-10 10:15:34 ERROR [SYS-3001]: Unknown system error
2024-04-10 10:15:35 INFO  [DONE] : Build finished
EOF

# Ensure file & directory permissions are readable by any non-root user
RUN chmod 644 /home/user/project/logs/build.log && \
    chmod -R a+rx /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8