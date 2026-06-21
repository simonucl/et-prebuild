FROM ubuntu:22.04

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/datasets/logs && \
    chmod 0755 /home/user/datasets/logs

RUN cat > /home/user/datasets/logs/collection.log <<'EOF'
[2023-02-14 10:12:03] SUCCESS BirdID: BD1001 URL: https://example.com/birds/BD1001.wav
[2023-03-01 07:45:56] SUCCESS BirdID: BD1042 URL: https://example.com/birds/BD1042.wav
[2023-04-22 19:10:11] SUCCESS BirdID: BD1100 URL: https://example.com/birds/BD1100.wav
[2023-06-30 22:51:42] SUCCESS BirdID: BD1155 URL: https://example.com/birds/BD1155.wav
[2023-12-01 05:02:29] SUCCESS BirdID: BD1300 URL: https://example.com/birds/BD1300.wav
[2022-11-20 08:00:00] SUCCESS BirdID: BD0900 URL: https://example.com/birds/BD0900.wav
[2023-01-02 12:00:07] FAIL    BirdID: BD1002 URL: https://example.com/birds/BD1002.wav
[2023-05-15 15:30:22] FAIL    BirdID: BD1120 URL: https://example.com/birds/BD1120.wav
[2021-07-14 03:03:03] SUCCESS BirdID: BD0500 URL: https://example.com/birds/BD0500.wav
EOF

RUN chmod 0644 /home/user/datasets/logs/collection.log && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH