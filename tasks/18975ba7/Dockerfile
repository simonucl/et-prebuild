FROM ubuntu:22.04

# Set non-interactive apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the user home directory structure
RUN mkdir -p /home/user/data

# Populate the CSV inventory file with the exact required contents
RUN cat > /home/user/data/iot_device_inventory.csv <<'CSVEND'
raspberry_pi,edge_node_01
raspberry_pi,edge_node_02
jetson_nano,edge_node_03
esp32,edge_node_04
raspberry_pi,edge_node_05
jetson_nano,edge_node_06
jetson_nano,edge_node_07
beaglebone_black,edge_node_08
esp32,edge_node_09
odroid_c2,edge_node_10
esp32,edge_node_11
beaglebone_black,edge_node_12
odroid_c2,edge_node_13
raspberry_pi,edge_node_14
esp32,edge_node_15
raspberry_pi,edge_node_16
CSVEND

# Ensure correct permissions
RUN chmod 644 /home/user/data/iot_device_inventory.csv && \
    chmod 755 /home/user

# Labels
LABEL Author="Edge-Computing Exercise Generator"
LABEL Description="Container image pre-provisioned with inventory data and pytest for automated grading."

# Set working directory
WORKDIR /home/user