# Author "Apptainer Task Builder"
# Description "Initial state container for the disk-usage report webserver task"
# This container sets up the initial environment for the disk-usage report exercise.
# It installs pytest for grading, creates the required /home/user/disk_reports/index.html file,
# and leaves everything else for the learner to complete.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/disk_reports

RUN cat >/home/user/disk_reports/index.html <<'EOF'
<html>
<head><title>Storage Report</title></head>
<body>
<h1>Storage Administrator Disk Usage Report</h1>
<p>This is a placeholder report.</p>
</body>
</html>
EOF

RUN chmod 0777 /home/user/disk_reports && \
    chmod 0644 /home/user/disk_reports/index.html

RUN useradd -m -u 1000 -d /home/user user || true && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin