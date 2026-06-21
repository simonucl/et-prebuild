# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This container is pre-loaded with:
#   • The raw TSV dataset at /home/user/datasets/raw_reviews.tsv
#   • GNU awk & sed
#   • Python 3 with pytest
#   Students can now carry out the processing task strictly from the shell.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip \
        gawk sed && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/datasets

RUN chmod 0777 /home/user && \
    chmod -R 0777 /home/user/datasets

RUN cat > /home/user/datasets/raw_reviews.tsv << 'EOF'
#id	text	label	extra
1	Hello World	POSITIVE	meta1
2	This is great	POSITIVE	meta2
#3	bad data	NEGATIVE
3	Awful	NEGATIVE	meta3
4	Lovely Day	POSITIVE	meta4

5	terrible	NEGATIVE	meta5
EOF

RUN chmod 0666 /home/user/datasets/raw_reviews.tsv

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Run script equivalent
CMD echo "Container for text-processing task." && \
    echo "Enter the container with a shell or run your commands directly."