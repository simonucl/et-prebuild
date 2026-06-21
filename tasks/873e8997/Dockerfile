FROM ubuntu:22.04

# Author ai-assistant
# Description "Environment for the cleaned-datasets backup exercise"

ENV PYTHONIOENCODING=UTF-8

RUN echo "alias python=python3" > /etc/profile.d/python_alias.sh

RUN set -e && \
    echo "Updating package lists and installing Python & system utilities..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir --upgrade pip pytest && \
    mkdir -p /home/user/datasets/cleaned

RUN cat << 'EOF' > /home/user/datasets/cleaned/iris_cleaned.csv
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
5.9,3.0,5.1,1.8,virginica
EOF

RUN cat << 'EOF' > /home/user/datasets/cleaned/titanic_cleaned.csv
survived,pclass,sex,age,fare
1,1,female,38,71.2833
0,3,male,34.5,7.8292
EOF

RUN cat << 'EOF' > /home/user/datasets/cleaned/mnist_cleaned.csv
pixel1,pixel2,pixel3,label
0,0,0,7
0,0,0,2
EOF

RUN chmod 755 /home/user /home/user/datasets /home/user/datasets/cleaned && \
    chmod 644 /home/user/datasets/cleaned/*.csv

CMD bash -c "echo 'Container for the cleaned-datasets backup exercise.' && echo 'You can now work on the task inside this container.' && exec \"\$@\""