FROM ubuntu:22.04

# Help / runscript notes
# Apptainer runscript:
# echo "Apptainer image for the 'mobile build benchmark' exercise."
# echo "Open a shell in the container and follow the task instructions."

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/mobile_build

RUN cat >/home/user/mobile_build/dummy_build.sh <<'EOF'
#!/usr/bin/env bash
# simple dummy build
sleep 1
echo "Dummy build finished"
EOF

RUN chmod 755 /home/user/mobile_build/dummy_build.sh

RUN chmod 777 /home/user/mobile_build

CMD /bin/sh -c "echo 'Apptainer image for the mobile build benchmark exercise.' && echo 'Open a shell in the container and follow the task instructions.'"