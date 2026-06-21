FROM ubuntu:22.04

# Maintainer ChatGPT
# Description "Initial state for artifact-deployment task. Provides /home/user/source/app.jar and pytest."

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN mkdir -p /home/user/source && \
    echo -n "dummy-artifact" > /home/user/source/app.jar && \
    chmod 644 /home/user/source/app.jar

RUN chmod 755 /home/user

CMD ["bash"]