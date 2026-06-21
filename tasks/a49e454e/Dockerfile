# Converted from Apptainer definition using base Ubuntu image
FROM ubuntu:22.04

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    mkdir -p /home/user/project/src && \
    mkdir -p /home/user/project/docs && \
    mkdir -p /home/user/project/tmp && \
    echo 'int main() { return 0; }' > /home/user/project/src/main.c && \
    echo 'void util() {}' > /home/user/project/src/util.c && \
    echo '# Project documentation' > /home/user/project/docs/readme.md && \
    echo 'Some temporary notes' > /home/user/project/tmp/notes.txt && \
    echo 'old tmp file' > /home/user/project/tmp/old.tmp && \
    echo 'backup of main.c' > /home/user/project/src/main.c.bak && \
    echo 'backup of util.c' > /home/user/project/src/util.c.bak && \
    echo 'backup of readme.md' > /home/user/project/docs/readme.md.bak && \
    echo 'backup of notes.txt' > /home/user/project/tmp/notes.txt.bak && \
    chmod -R 0777 /home/user

# Environment section
ENV HOME=/home/user
RUN chmod 755 /home/user

# Labels
LABEL Author="example@example.com"
LABEL Task="find | xargs cleanup challenge"

# Help section
# This container sets up a small project directory under /home/user/project
# containing four “*.bak” files that must be removed by the student using a
# single “find | xargs” command, while logging the deleted paths. Pytest is
# pre-installed so the grading tests can run.