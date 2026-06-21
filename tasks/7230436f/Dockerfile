FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/docs

RUN printf 'Frequently-asked questions draft.\n' > /home/user/docs/faq_draft.txt && \
    printf 'Introduction section draft.\n' > /home/user/docs/intro_draft.txt && \
    printf 'Usage instructions draft.\n' > /home/user/docs/usage_draft.txt

RUN chmod -R 0777 /home/user/docs

RUN chmod 755 /home/user

ENV LANG=C.UTF-8

CMD ["echo", "Apptainer container ready for the batch-rename task."]