FROM ubuntu:22.04

LABEL Author="you"
LABEL Description="Initial filesystem for deployment changelog exercise with pytest installed"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

ENV BASE=/home/user

RUN mkdir -p /home/user/deployment/releases && \
    mkdir -p /home/user/deployment/config && \
    mkdir -p /home/user/deployment/releases/v1.0.0 && \
    mkdir -p /home/user/deployment/releases/v1.1.0 && \
    mkdir -p /home/user/deployment/releases/v1.2.0

RUN cat > /home/user/deployment/releases/v1.0.0/NOTES.md <<'EOF'
FEATURE: Add login functionality
FEATURE: Add logout functionality
FIX: Correct typo in README
EOF

RUN cat > /home/user/deployment/releases/v1.1.0/NOTES.md <<'EOF'
FEATURE: Add password reset
EOF

RUN cat > /home/user/deployment/releases/v1.2.0/NOTES.md <<'EOF'
FEATURE: Improve UI
FIX: Fix crash on launch
FEATURE: Add dark mode
FIX: Memory leak fix
FEATURE: Optimize database queries
EOF

RUN cat > /home/user/deployment/config/app.conf <<'EOF'
# Application configuration
environment=staging
# the version key will be added/updated by the agent
EOF

RUN chmod -R a+rX /home/user/deployment

RUN chmod 755 /home/user

# Build-time test: verify pytest is importable
RUN python3 -c "import pytest; print('pytest version:', pytest.__version__)"

CMD ["echo", "Container for deployment changelog exercise. No default runscript."]