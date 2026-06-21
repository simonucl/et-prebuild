FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/data/raw

# Populate TSV: user_features.tsv
RUN cat > /home/user/data/raw/user_features.tsv << 'EOF'
id	age	height_cm	weight_kg
1	25	175	70
2	31	168	80
3	22	180	75
EOF

# Populate TSV: activity_stats.tsv
RUN cat > /home/user/data/raw/activity_stats.tsv << 'EOF'
id	avg_daily_steps	max_heart_rate
1	8000	190
2	6500	180
3	12000	200
EOF

# Fix permissions
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PYTHONIOENCODING=utf-8

# Default runscript behavior
CMD echo "Container for data-processing task. Start an interactive shell:" && exec /bin/bash