# Author: Container pre-population for data-cleaning task
# Description: Sets up the initial directory tree and installs pytest.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir -U pip pytest

RUN mkdir -p /home/user/datasets/raw && \
    mkdir -p /home/user/datasets/clean

RUN echo -e "id,name\n1,Alice" > /home/user/datasets/raw/customers.csv && \
    echo -e "sku,stock\n001,50" > /home/user/datasets/raw/inventory.csv && \
    echo -e "id,product,price\n1,Pen,1.20" > /home/user/datasets/raw/products.csv && \
    echo -e "id,date,total\n1,2023-01-01,100" > /home/user/datasets/raw/sales.csv && \
    echo '{ "note": "sample content" }' > /home/user/datasets/raw/notes.json

RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

CMD echo "This container is prepared for the data-cleaning task." && \
    echo "Use 'docker run -it ... bash' to get a shell."