FROM ubuntu:22.04

# Help section (from Apptainer %help, if any was present)
# No %help content provided.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/cloud_costs && \
    printf 'aws,2023-09,123.45\n'  > /home/user/cloud_costs/aws_cost_report.csv && \
    printf 'azure,2023-09,67.89\n' > /home/user/cloud_costs/azure_cost_report.csv && \
    printf 'gcp,2023-09,45.67\n'   > /home/user/cloud_costs/gcp_cost_report.csv && \
    chmod 755 /home/user && \
    chmod 755 /home/user/cloud_costs && \
    chmod 644 /home/user/cloud_costs/*.csv