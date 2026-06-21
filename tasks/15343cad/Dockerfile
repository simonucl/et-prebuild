FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/builds/2023-05-01 && \
    mkdir -p /home/user/builds/2023-05-02 && \
    mkdir -p /home/user/builds/2023-05-03

# 2023-05-01 log
RUN cat <<'EOF' > /home/user/builds/2023-05-01/artifacts.log
app-core|1.0.0|1500|abc111|OK
app-ui|1.0.0|500|def222|FAIL
lib-utils|2.1.3|300|ghi333|OK
EOF

# 2023-05-02 log
RUN cat <<'EOF' > /home/user/builds/2023-05-02/artifacts.log
app-core|1.0.1|1520|abc444|OK
app-ui|1.0.1|520|def555|OK
lib-utils|2.1.3|300|ghi333|FAIL
plugin-auth|0.9.0|200|jkl666|OK
EOF

# 2023-05-03 log
RUN cat <<'EOF' > /home/user/builds/2023-05-03/artifacts.log
app-core|1.0.1|1520|abc777|FAIL
plugin-auth|0.9.1|210|jkl999|OK
EOF

# Permissions
RUN chmod -R 777 /home/user && \
    chmod 666 /home/user/builds/2023-05-*/artifacts.log

# From %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Help text from %runscript (commented)
# Container ready for the build-log processing task.
# Enter an interactive shell with: apptainer exec <image> /bin/bash

# Labels
LABEL Author="ChatGPT"
LABEL Description="Ubuntu 22.04 base with pytest installed and initial build-log data for the artifacts task."