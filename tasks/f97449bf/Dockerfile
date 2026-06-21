FROM ubuntu:22.04

# From %help
# This container image sets up a small PHP web-app under /home/user/webapp
# and installs pytest for automated evaluation.

ENV HOME=/home/user

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0777 /home/user

# Create webapp directories
RUN mkdir -p /home/user/webapp/admin

# Create index.php
RUN WEBAPP="/home/user/webapp" && \
    INDEX_PHP="${WEBAPP}/index.php" && \
    : > "$INDEX_PHP" && \
    echo "<?php" >> "$INDEX_PHP" && \
    for i in $(seq 2 13); do echo "// line ${i}" >> "$INDEX_PHP"; done && \
    echo "eval(\$_GET['run']);" >> "$INDEX_PHP" && \
    for i in $(seq 15 18); do echo "// line ${i}" >> "$INDEX_PHP"; done

# Create admin/tools.php
RUN WEBAPP="/home/user/webapp" && \
    TOOLS_PHP="${WEBAPP}/admin/tools.php" && \
    : > "$TOOLS_PHP" && \
    echo "<?php" >> "$TOOLS_PHP" && \
    for i in $(seq 2 44); do echo "// line ${i}" >> "$TOOLS_PHP"; done && \
    echo "exec(\$cmd);" >> "$TOOLS_PHP" && \
    for i in $(seq 46 59); do echo "// line ${i}" >> "$TOOLS_PHP"; done && \
    echo "eval(\$dangerous);" >> "$TOOLS_PHP" && \
    for i in $(seq 61 70); do echo "// line ${i}" >> "$TOOLS_PHP"; done

RUN chmod -R a+rwX /home/user

# Labels
LABEL Author="SecurityExercisePrep"
LABEL Description="Container prepared for the 'quick static security sweep' exercise"