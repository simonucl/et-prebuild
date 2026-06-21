FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip install --no-cache-dir pytest

# Create base user home directory
RUN mkdir -p /home/user

# Set up initial workspace expected by the tests
RUN mkdir -p /home/user/research_datasets/climate_data && \
    mkdir -p /home/user/research_datasets/ocean_salinity && \
    mkdir -p /home/user/research_datasets/star_catalog && \
    touch /home/user/research_datasets/climate_data/data.csv && \
    touch /home/user/research_datasets/ocean_salinity/salinity.csv && \
    touch /home/user/research_datasets/star_catalog/stars.parquet

# meta.json for climate_data
RUN cat > /home/user/research_datasets/climate_data/meta.json <<'EOF'
{
  "description": "Daily world surface temperature readings.",
  "rows": 36500,
  "columns": 8
}
EOF

# meta.json for ocean_salinity
RUN cat > /home/user/research_datasets/ocean_salinity/meta.json <<'EOF'
{
  "description": "Global ocean surface salinity measurements.",
  "rows": 54000,
  "columns": 6
}
EOF

# meta.json for star_catalog
RUN cat > /home/user/research_datasets/star_catalog/meta.json <<'EOF'
{
  "description": "Stellar positions and magnitudes from deep-sky survey.",
  "rows": 112000,
  "columns": 12
}
EOF

# Ensure permissions
RUN chmod -R a+rX /home/user && chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default action mimic runscript
CMD ["bash"]