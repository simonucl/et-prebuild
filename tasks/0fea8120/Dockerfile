FROM ubuntu:22.04

# Update package index and install Python tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools && \
    pip3 install --no-cache-dir pytest

# Prepare initial directory structure and raw CSV files for tests
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN mkdir -p /home/user/raw_data && \
    chmod 0755 /home/user/raw_data

RUN printf "time,signal\n0,0.123\n" > /home/user/raw_data/dataset_A_v1.csv
RUN printf "time,value\n0,42.7\n" > /home/user/raw_data/dataset_B_v1.csv

RUN chmod 0644 /home/user/raw_data/dataset_A_v1.csv /home/user/raw_data/dataset_B_v1.csv

# Default command similar to %runscript
CMD ["bash"]