FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create directory tree
RUN mkdir -p /home/user/opt_project/src/models && \
    mkdir -p /home/user/opt_project/data && \
    mkdir -p /home/user/opt_project/tests && \
    mkdir -p /home/user/opt_project/legacy

# Create placeholder files
RUN echo "Project README" > /home/user/opt_project/README.md
RUN echo "from setuptools import setup" > /home/user/opt_project/setup.py
RUN echo "def solve(): pass" > /home/user/opt_project/src/solver.py
RUN echo "\* Model A LP content *\\" > /home/user/opt_project/src/models/modelA.lp
RUN echo "\* Model B MPS content *\\" > /home/user/opt_project/src/models/modelB.mps
RUN echo "demand,quantity" > /home/user/opt_project/data/demand.csv
RUN echo "\* Scenario LP *\\" > /home/user/opt_project/data/scenario.lp
RUN echo "def test_parser():\n    assert True" > /home/user/opt_project/tests/test_parser.py
RUN echo "\* Legacy MPS *\\" > /home/user/opt_project/legacy/old_model.mps

# Permissions
RUN chmod -R 777 /home/user/opt_project && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run script equivalent
CMD echo "Container for optimisation-project task."