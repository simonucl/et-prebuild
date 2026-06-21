FROM ubuntu:22.04

# Help section:
# This container sets up an evidence directory at /home/user/forensics
# containing a Latin-1 encoded text file.  Students must convert the
# file to UTF-8 and generate the required status log, as described in
# the assignment.

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip locales && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/forensics && \
    chmod 0777 /home/user/forensics

RUN cat > /tmp/incident_note_utf8.txt <<'EOF'
Incident Note - 2023-05-15
Affected user: José Álvarez
Issue: Crème brûlée recipe overwritten with mojibake
Details: ½ cup sugar became ÃÂ½ cup sugar
Resolution: Convert file encoding from ISO-8859-1 to UTF-8.
EOF

RUN iconv -f UTF-8 -t ISO-8859-1 /tmp/incident_note_utf8.txt \
        > /home/user/forensics/incident_note_latin1.txt && \
    chmod 0666 /home/user/forensics/incident_note_latin1.txt && \
    rm -f /tmp/incident_note_utf8.txt && \
    chmod 755 /home/user

LABEL Author="incident-response-prep"