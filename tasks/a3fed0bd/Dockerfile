FROM ubuntu:22.04

# Help:
# This container provides the initial filesystem state required for the
# checksum-manifest task. Students will create a manifest of all *.js files
# under /home/user/webapp. Pytest is pre‑installed for automated grading.

LABEL Author="task-preparer"
LABEL Description="Container for the JavaScript checksum pipeline task – includes prepared project and pytest"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN install -d -m 0777 /home/user/webapp && \
    install -d -m 0755 /home/user/webapp/assets/js && \
    install -d -m 0755 /home/user/webapp/src/utils

RUN cat <<'EOF' > /home/user/webapp/assets/js/script1.js
console.log('Script One');
EOF

RUN cat <<'EOF' > /home/user/webapp/assets/js/script2.js
console.log('Script Two');
EOF

RUN cat <<'EOF' > /home/user/webapp/src/app.js
console.log('Main App');
EOF

RUN cat <<'EOF' > /home/user/webapp/src/utils/helper.js
export function greet() { return 'Hello'; }
EOF

RUN cat <<'EOF' > /home/user/webapp/README.md
# Sample project
EOF

RUN chmod -R a+rX /home/user/webapp && \
    chmod 755 /home/user