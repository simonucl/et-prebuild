# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author label from Apptainer %labels
LABEL Author="Container prepared for ML dashboard task"

# --------------------------------------------------------------------
# Install Python, pip, and pytest
# --------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------
# Create the default user
# --------------------------------------------------------------------
RUN useradd -m -s /bin/bash user

# --------------------------------------------------------------------
# Seed experiment data expected by the assessment tests
# --------------------------------------------------------------------
RUN mkdir -p /home/user/experiments/exp_alpha \
             /home/user/experiments/exp_beta \
             /home/user/experiments/exp_gamma

# exp_alpha metrics.csv
RUN cat > /home/user/experiments/exp_alpha/metrics.csv <<'EOF'
epoch,loss,accuracy
1,0.65,0.70
2,0.60,0.75
3,0.58,0.78
EOF

# exp_beta metrics.csv
RUN cat > /home/user/experiments/exp_beta/metrics.csv <<'EOF'
epoch,loss,accuracy
1,0.55,0.72
2,0.50,0.80
3,0.48,0.82
4,0.47,0.83
5,0.46,0.84
EOF

# exp_gamma metrics.csv
RUN cat > /home/user/experiments/exp_gamma/metrics.csv <<'EOF'
epoch,loss,accuracy
1,0.70,0.68
2,0.65,0.70
3,0.63,0.72
4,0.62,0.74
EOF

# --------------------------------------------------------------------
# Permissions
# --------------------------------------------------------------------
RUN chmod -R a+rX /home/user/experiments && \
    chmod a+w /home/user/experiments && \
    chmod 755 /home/user

# --------------------------------------------------------------------
# Environment variables (from %environment)
# --------------------------------------------------------------------
ENV PATH=/home/user/.local/bin:$PATH