FROM ubuntu:22.04

# Update package lists and install Python tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the directory structure
RUN mkdir -p /home/user/datasets

# Create the raw_sales.tsv file with the exact required contents
RUN cat > /home/user/datasets/raw_sales.tsv <<'EOF'
Region	Product	Q1	Q2	Q3	Q4	Notes
North	Widget	1200	1300	1400	1500	High demand
South	Gadget	900	950	970	980	Backordered
East	Widget	1100	1150	1200	1250	Stable
West	Gadget	1000	1020	1040	1050	Promotion planned
EOF

# Set conservative permissions so the non-root runtime user can read/write
RUN chmod 755 /home/user && \
    chmod 755 /home/user/datasets && \
    chmod 644 /home/user/datasets/raw_sales.tsv

# Environment variables
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin