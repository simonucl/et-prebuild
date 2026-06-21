FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Dataset scaffolding
RUN mkdir -p /home/user/datasets/raw

# iris.csv
RUN cat <<'EOF' > /home/user/datasets/raw/iris.csv
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
EOF

# mtcars.csv
RUN cat <<'EOF' > /home/user/datasets/raw/mtcars.csv
model,mpg,cyl,disp,hp,drat,wt,qsec,vs,am,gear,carb
Mazda RX4,21.0,6,160.0,110,3.90,2.620,16.46,0,1,4,4
Mazda RX4 Wag,21.0,6,160.0,110,3.90,2.875,17.02,0,1,4,4
Datsun 710,22.8,4,108.0,93,3.85,2.320,18.61,1,1,4,1
Hornet 4 Drive,21.4,6,258.0,110,3.08,3.215,19.44,1,0,3,1
EOF

# Permissions
RUN chmod -R a+rwX /home/user

# Environment
ENV PYTHONUNBUFFERED=1
RUN chmod 755 /home/user