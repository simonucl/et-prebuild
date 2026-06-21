FROM ubuntu:22.04

# HELP: Container for Iris checksum assignment.

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/training_data/raw

RUN cat << 'EOF' > /home/user/training_data/raw/iris_train.csv
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
6.2,3.4,5.4,2.3,virginica
EOF

RUN cat << 'EOF' > /home/user/training_data/raw/iris_valid.csv
sepal_length,sepal_width,petal_length,petal_width,species
5.4,3.9,1.3,0.4,setosa
6.0,2.2,4.0,1.0,versicolor
6.9,3.1,5.1,2.3,virginica
EOF

RUN cat << 'EOF' > /home/user/training_data/raw/iris_test.csv
sepal_length,sepal_width,petal_length,petal_width,species
4.8,3.0,1.4,0.3,setosa
5.5,2.3,4.0,1.3,versicolor
7.2,3.0,5.8,1.6,virginica
EOF

RUN chmod 755 /home/user && chmod -R 755 /home/user/training_data && chmod 644 /home/user/training_data/raw/*.csv

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# RUNSCRIPT equivalent
CMD ["echo", "Container for Iris checksum assignment. Invoke your own commands."]