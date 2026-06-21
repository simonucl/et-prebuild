FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the “avian flu dataset” exercise
RUN mkdir -p /home/user/raw_data

RUN echo "id,country,date,cases" > /home/user/raw_data/avian_flu_cases.csv
RUN echo "source,contact,email" > /home/user/raw_data/avian_flu_metadata.csv

# Ensure permissions
RUN chmod -R a+rwX /home/user

RUN chmod 755 /home/user

CMD ["/bin/bash"]