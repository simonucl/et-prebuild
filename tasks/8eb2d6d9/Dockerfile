FROM ubuntu:22.04

LABEL Author="climate-task-setup"
LABEL Description="Container for climate data structuring task. Provides initial filesystem state and installs pytest."

# 1. Install required packages and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Create non-root user `user`
RUN useradd -m -s /bin/bash user

# 3. Set up initial directory tree and files
RUN mkdir -p /home/user/downloads && \
    mkdir -p /home/user/research

# Climate temperature v1
RUN cat >/home/user/downloads/climate_temp_v1.txt <<'EOF'
date,temp
2024-01-01,23
2024-01-02,22
EOF

# Climate temperature v2
RUN cat >/home/user/downloads/climate_temp_v2.txt <<'EOF'
date,temp
2024-01-01,24
2024-01-02,23
2024-01-03,25
EOF

# Climate precipitation v1
RUN cat >/home/user/downloads/climate_precip_v1.txt <<'EOF'
date,precip_mm
2024-01-01,5
2024-01-02,0
EOF

# Unrelated README that must stay untouched
RUN echo "Placeholder README – do not move." >/home/user/downloads/readme.txt

# Ensure proper ownership so the non-root agent can work freely
RUN chown -R user:user /home/user

# Set permissions and environment
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH