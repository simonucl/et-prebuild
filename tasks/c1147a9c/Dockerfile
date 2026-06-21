FROM ubuntu:22.04

# This container pre-stages a small front-end project under /home/user/web_project
# and has Python/pytest available for automated grading.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        zip \
        tar && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/web_project/css && \
    mkdir -p /home/user/web_project/js && \
    mkdir -p /home/user/web_project/images

# index.html (100 bytes)
RUN cat > /home/user/web_project/index.html <<'EOF'
<!DOCTYPE html>
<html>
<head><title>Demo</title></head>
<body>
<h1>Hello World</h1>
</body>
</html>
EOF

# css/style.css (41 bytes)
RUN cat > /home/user/web_project/css/style.css <<'EOF'
body { font-family: Arial, sans-serif; }
EOF

# js/app.js (28 bytes)
RUN cat > /home/user/web_project/js/app.js <<'EOF'
console.log('Hello World');
EOF

# images/logo.png (22 bytes - placeholder text)
RUN cat > /home/user/web_project/images/logo.png <<'EOF'
PNG IMAGE PLACEHOLDER
EOF

# Ensure non-root users can work inside /home/user
RUN chmod -R 777 /home/user

WORKDIR /home/user

CMD ["/bin/bash"]