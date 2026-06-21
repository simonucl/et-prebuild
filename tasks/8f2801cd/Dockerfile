FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Container image pre-seeded for the SRE monitor JSON conversion exercise"

# Help text
# This image contains:
#   • Python 3 and pytest installed system-wide.
#   • Pre-seeded INI configuration at /home/user/sre_monitor/config/services.ini
# Students will read this INI file and generate the required JSON output.

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/sre_monitor/config

RUN cat <<'EOF' > /home/user/sre_monitor/config/services.ini
[web]
name = frontend
host = 127.0.0.1
port = 80

[db]
name = database
host = 127.0.0.1
port = 5432

[external_dns]
name = google_dns
host = 8.8.8.8
port = 53
EOF

RUN chmod -R 755 /home/user/sre_monitor && chmod 644 /home/user/sre_monitor/config/services.ini

RUN chmod 755 /home/user

ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8