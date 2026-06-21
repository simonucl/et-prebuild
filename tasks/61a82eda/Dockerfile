FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# --------------------------------------------------------------------- #
# Prepare initial exercise data under /home/user/data/staging
# --------------------------------------------------------------------- #
RUN mkdir -p /home/user/data/staging/nested

# Five *.tmp files
RUN printf "temporary readme\n" > /home/user/data/staging/readme.tmp && \
    printf "some notes\n" > /home/user/data/staging/notes.tmp && \
    : > /home/user/data/staging/empty.tmp && \
    printf "old tmp\n" > /home/user/data/staging/nested/old.tmp && \
    : > /home/user/data/staging/nested/blank.tmp

# Three *.txt files
RUN printf "sample1-data\n" > /home/user/data/staging/sample1.txt && \
    printf "sample2-data\n" > /home/user/data/staging/sample2.txt && \
    printf "nested-sample\n" > /home/user/data/staging/nested/data.txt

# One log file that must remain untouched by the agent
RUN printf "keep me\n" > /home/user/data/staging/ignore.log

# Ensure the learner (non-root user) can freely manipulate everything
RUN chmod -R a+rwX /home/user

ENV HOME=/home/user

WORKDIR /home/user

# Default runscript – drop into a shell
CMD ["/bin/bash"]