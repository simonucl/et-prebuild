FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer setup - ChatGPT"
LABEL Description="Ubuntu 22.04 environment pre-populated with starter CSV, pytest, and utilities for a sales data processing exercise."

# Help information (as comments):
# This container provides the initial environment for the sales data
# processing task.  The directory /home/user/project contains the
# starter file raw_sales.csv.  No other output artefacts are present.
# Python (with pytest, csvkit, jsonschema) and jq are pre-installed.
# Run the container and complete the exercise as instructed.

RUN set -e && \
    echo "Updating apt repositories and installing packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates \
        locales && \
    sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8

RUN echo "Installing Python packages..." && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest csvkit jsonschema

RUN echo "Creating project directory and starter CSV..." && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    mkdir -p /home/user/project && \
    chmod 0755 /home/user/project

RUN cat > /home/user/project/raw_sales.csv <<'CSVEND'
Date,Region,Rep,Item,Units,Unit Cost,Total
2023-07-01,East,Jones,Pencil,95,1.99,189.05
2023-07-02,West,Kivell,Binder,50,19.99,999.50
2023-07-03,East,Jardine,Pencil,36,4.99,179.64
2023-07-04,East,Gill,Pen,27,19.99,539.73
2023-07-05,Central,Sorvino,Pencil,56,2.99,167.44
2023-07-06,East,Jones,Binder,60,4.99,299.40
2023-07-07,West,Andrews,Pencil,75,1.99,149.25
2023-07-08,Central,Jardine,Pen Set,90,15.99,1439.10
2023-07-09,Central,Thompson,Binder,32,4.99,159.68
2023-07-10,East,Jones,Pencil,65,4.99,324.35
CSVEND

RUN chmod 0644 /home/user/project/raw_sales.csv

RUN echo "Cleaning up apt cache..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

WORKDIR /home/user

CMD ["bash", "-c", "echo 'Container for Sales Data Processing Exercise' && echo 'Navigate to /home/user/project to begin.' && exec bash"]