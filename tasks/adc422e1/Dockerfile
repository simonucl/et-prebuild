FROM ubuntu:22.04

# Labels
LABEL Author="security-eng-task"
LABEL Description="Initial environment for credential rotation exercise."

# Help section as comments:
# This container sets up the initial state for a credential rotation task.
# Use it to practice updating configuration files and logging rotations.

# Update package lists and install Python 3 and pip.
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip

# Install pytest for the test-runner.
RUN pip3 install --no-cache-dir pytest

# Establish the initial filesystem state expected by the test suite.
RUN mkdir -p /home/user/app/config

# Create /home/user/app/config/settings.yaml with the original values.
RUN cat > /home/user/app/config/settings.yaml <<'EOF'
database:
  host: db.prod.internal
  username: admin
  password: OldPassword123!
EOF

# Ensure the file ends with exactly one trailing newline.
RUN sed -i -e '$a\' /home/user/app/config/settings.yaml

# Create /home/user/app/config/secrets.toml with the original values.
RUN cat > /home/user/app/config/secrets.toml <<'EOF'
[api]
token = "old_api_token_ABC123"
expiry = "2024-12-31T23:59:59Z"
EOF

# Ensure the file ends with exactly one trailing newline.
RUN sed -i -e '$a\' /home/user/app/config/secrets.toml

# rotation.log must NOT exist at build time, per test requirements.

# Make sure the non-root user (same UID as host) can write inside /home/user.
RUN chmod -R 0777 /home/user

# Clean up apt cache to keep the image small.
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Runscript equivalent
CMD chmod 755 /home/user && echo "Container ready. Execute your tasks inside the shell."