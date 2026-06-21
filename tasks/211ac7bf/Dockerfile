FROM ubuntu:22.04

# Update APT index and install Python tooling
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial directory / file structure for the exercise
RUN mkdir -p /home/user && \
    mkdir -p /home/user/datasets/astronomy && \
    mkdir -p /home/user/datasets/climate && \
    mkdir -p /home/user/datasets/epidemiology

# Create astronomy dataset
RUN echo -e "id\tname\tmagnitude\n1\tMilkyWay\t-20.9" > /home/user/datasets/astronomy/galaxies.tsv

# Create climate dataset
RUN echo "date,temp_c" > /home/user/datasets/climate/temp.csv && \
    echo "date,rain_mm" > /home/user/datasets/climate/rainfall.csv

# Create epidemiology dataset
RUN echo "week,cases" > /home/user/datasets/epidemiology/flu_2020.csv && \
    echo "week,cases" > /home/user/datasets/epidemiology/covid_2020.csv && \
    echo "week,cases" > /home/user/datasets/epidemiology/measles_2019.csv

# Permissions adjustments
RUN chmod -R a+rX /home/user && \
    chmod -R u+w /home/user && \
    chmod a+rwx /home/user

# Environment settings
RUN chmod 755 /home/user
ENV PATH="/usr/bin:$PATH"

# Help text from %runscript
# Container for the 'dataset manifest' exercise.
# Run your commands inside this container to generate /home/user/dataset_manifest.tsv.

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment prepared for the dataset manifest exercise"