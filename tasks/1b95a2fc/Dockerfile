# Author: TaskPreparer
# Description: Base image for CSV-permissions exercise. Provides initial raw data and pytest.
# Help:
#   This container is the starting point for the “CSV permissions and cleaning” task.
#   It already contains:
#     • /home/user/datasets/raw/data1.csv
#     • /home/user/datasets/raw/data2.csv
#   Both files are in their initial state (mode 644).

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/datasets/raw

RUN cat <<'EOF' > /home/user/datasets/raw/data1.csv
id,value
1,23
2,
3,45
EOF

RUN cat <<'EOF' > /home/user/datasets/raw/data2.csv
id,value,score
1,10,0.5
2,,0.7
3,12,
EOF

RUN chmod 644 /home/user/datasets/raw/data1.csv && \
    chmod 644 /home/user/datasets/raw/data2.csv

# Equivalent of %runscript (no default behavior needed)
RUN chmod 755 /home/user

CMD echo "Container for CSV-permissions exercise. Nothing to run by default."