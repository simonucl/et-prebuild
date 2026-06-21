FROM ubuntu:22.04

# Help and labels from %labels
# Author: Built by AI
# Description: Apptainer image for config update task – provides initial files and pytest.

ENV DEBIAN_FRONTEND=noninteractive

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/app/config

RUN cat <<'EOF' > /home/user/projects/app/config/default.yaml
app:
  name: SampleApp
  environments:
    development:
      host: localhost
      debug: true
      version: 1.4
EOF

RUN echo >> /home/user/projects/app/config/default.yaml

RUN cat <<'EOF' > /home/user/projects/app/config/settings.toml
[app]
name = "SampleApp"

[app.environments.development]
host = "localhost"
debug = true
version = "1.4"
EOF

RUN echo >> /home/user/projects/app/config/settings.toml

RUN chmod -R a+rwX /home/user && chmod 755 /home/user