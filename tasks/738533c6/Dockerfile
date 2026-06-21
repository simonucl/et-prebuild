FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Description="Environment for \"Synchronize a Mock Remote Web Root\" task."

# Install Python tooling (pytest required by grader)
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip coreutils && \
    pip3 install --no-cache-dir pytest

# Prepare writable HOME for the learner
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Construct the mock "remote" web root
RUN mkdir -p /home/user/mock_remote/var/www/html/admin /home/user/mock_remote/var/www/html/css

# Create index.php (1254 bytes)
RUN cat > /home/user/mock_remote/var/www/html/index.php <<'PHP'
<?php
echo "Welcome to vulnerable VM!";
// ...
PHP

RUN truncate -s 1254 /home/user/mock_remote/var/www/html/index.php

# Create admin/login.php (2048 bytes)
RUN cat > /home/user/mock_remote/var/www/html/admin/login.php <<'PHP'
<?php
session_start();
// ...
PHP

RUN truncate -s 2048 /home/user/mock_remote/var/www/html/admin/login.php

# Create css/style.css (512 bytes)
RUN cat > /home/user/mock_remote/var/www/html/css/style.css <<'CSS'
body {
    background:#222;
}
/* ... */
CSS

RUN truncate -s 512 /home/user/mock_remote/var/www/html/css/style.css

# Ensure readability
RUN chmod -R a+rX /home/user/mock_remote

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for the synchronization task is ready."]