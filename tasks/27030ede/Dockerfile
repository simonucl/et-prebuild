# Help: IoT dashboard scraping utility setup
# Author: Scraping-Utility Setup
# Description: Provides fixture HTML pages and pytest for the scraping assignment.

FROM ubuntu:22.04

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 755 /home/user && \
    mkdir -p /home/user/iot_dashboard/pages && \
    chmod 755 /home/user/iot_dashboard && \
    chmod 755 /home/user/iot_dashboard/pages

RUN cat <<'EOF' > /home/user/iot_dashboard/pages/device_001.html
<html><body><span id="device-id">001</span><span id="temp">23.7</span><span id="hum">50</span><span id="bat">87</span><span id="ts">2024-03-11T15:04:22Z</span></body></html>
EOF

RUN cat <<'EOF' > /home/user/iot_dashboard/pages/device_002.html
<html><body><span id="device-id">002</span><span id="temp">21.9</span><span id="hum">49</span><span id="bat">92</span><span id="ts">2024-03-11T15:04:34Z</span></body></html>
EOF

RUN cat <<'EOF' > /home/user/iot_dashboard/pages/device_003.html
<html><body><span id="device-id">003</span><span id="temp">24.5</span><span id="hum">48</span><span id="bat">90</span><span id="ts">2024-03-11T15:04:47Z</span></body></html>
EOF

RUN chmod 644 /home/user/iot_dashboard/pages/device_*.html

RUN sed -i 's/# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen