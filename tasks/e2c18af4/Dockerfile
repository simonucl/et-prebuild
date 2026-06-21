FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the predefined deployment directory and solver stub
RUN mkdir -p /home/user/optim && \
    chmod 755 /home/user && \
    chmod 755 /home/user/optim

RUN cat > /home/user/optim/update_lp.py << 'EOF'
#!/usr/bin/env python3
"""
Tiny smoke-test LP solver stub shipped with every deployment.
DO NOT EDIT.
"""
def main():
    print("SOLVER_OK objective=1764")
if __name__ == "__main__":
    main()
EOF

RUN chmod 755 /home/user/optim/update_lp.py

# Give a non-root default user (UID 1000) ownership so that the runtime
# user—typically UID 1000 in many CI systems—has write access while
# retaining the required 0755 permissions.
RUN chown -R 1000:1000 /home/user || true

# Container set-up for the "smoke-test LP solver" exercise.
# Provides:
#   • Pre-seeded /home/user/optim/update_lp.py (executable, mode 755).
#   • pytest available system-wide.
# No other artefacts are created; the student will generate
# /home/user/optim/verification.log during the task.