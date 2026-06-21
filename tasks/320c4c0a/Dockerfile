FROM ubuntu:22.04

# Author TaskSetup
# Description "Environment for packaging exercise – pre-populated release tree and pytest installed"
# This container provides the initial filesystem state for the packaging
# exercise. The release files are located under /home/user/releases/v2 and
# pytest is pre-installed so the grading tests can run.

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/releases/v2/scripts

RUN cat <<'EOF' > /home/user/releases/v2/README.md
# App v2 Update
This release fixes bugs and improves performance.
EOF

RUN cat <<'EOF' > /home/user/releases/v2/app.conf
version=2.0.1
environment=production
debug=false
EOF

RUN cat <<'EOF' > /home/user/releases/v2/scripts/start.sh
#!/bin/bash
echo "Starting App v2..."
EOF

RUN chmod +x /home/user/releases/v2/scripts/start.sh

RUN chmod -R a+rwX /home/user

RUN chmod 755 /home/user

ENV PYTHONPATH=""
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

CMD ["/bin/bash"]