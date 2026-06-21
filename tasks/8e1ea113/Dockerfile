FROM ubuntu:22.04

# Help / runscript notes from Apptainer
# Container ready. Launch a shell to perform the deployment-log task.

RUN set -e

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/deploy/releases/v2.3.1 && \
    mkdir -p /home/user/deploy/releases/v2.4.0 && \
    mkdir -p /home/user/deploy/releases/v2.4.1

RUN cat <<'EOF' > /home/user/deploy/releases/v2.3.1/release_notes.md
# Release v2.3.1
Date: 2023-04-17
- Fixed issue with authentication timeout
- Improved logging around API errors
EOF

RUN cat <<'EOF' > /home/user/deploy/releases/v2.4.0/release_notes.md
# Release v2.4.0
Date: 2023-05-29
- Added support for PostgreSQL 14
- Deprecated legacy report generator
EOF

RUN cat <<'EOF' > /home/user/deploy/releases/v2.4.1/release_notes.md
# Release v2.4.1
Date: 2023-06-12
- Hotfix: Corrected SQL migration script for user_profiles table
EOF

RUN chmod 0777 /home/user/deploy && \
    chmod -R a+rX /home/user/deploy/releases

CMD ["bash"]