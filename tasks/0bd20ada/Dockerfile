FROM ubuntu:22.04

# Author example
# Description "Setup initial dataset and environment for TSV column-extraction task"

ENV PATH="$PATH:$HOME/.local/bin"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/datasets && \
    chmod 777 /home/user && \
    chmod 777 /home/user/datasets

RUN printf 'gene_id\tgene_name\tchromosome\n1\tTP53\t17\n2\tEGFR\t7\n3\tBRCA1\t17\n4\tMYC\t8\n5\tMTOR\t1\n' \
        > /home/user/datasets/genes.tsv

RUN printf 'gene_id\tsample_A\tsample_B\tsample_C\n1\t12.5\t13.0\t11.8\n2\t4.2\t4.9\t5.0\n3\t7.7\t8.1\t7.5\n4\t20.0\t19.5\t21.1\n5\t10.3\t9.8\t10.0\n' \
        > /home/user/datasets/expression.tsv

RUN printf 'sample_id\ttissue\tcondition\nsample_A\tliver\ttreated\nsample_B\tliver\tcontrol\nsample_C\theart\ttreated\n' \
        > /home/user/datasets/sample_info.tsv

RUN chmod 0644 /home/user/datasets/genes.tsv && \
    chmod 0644 /home/user/datasets/expression.tsv && \
    chmod 0644 /home/user/datasets/sample_info.tsv && \
    chmod 755 /home/user

CMD echo "Container for TSV column-extraction task." && echo "Enter the shell with: docker run -it <image> /bin/bash"