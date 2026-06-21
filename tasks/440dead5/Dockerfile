FROM ubuntu:22.04

# Help section from Apptainer runscript
# Original runscript: chmod 755 /home/user ; exec /bin/bash

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN chmod 755 /home/user

CMD ["/bin/bash"]