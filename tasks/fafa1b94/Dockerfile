FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the required directory tree
RUN mkdir -p /home/user/data/csvs/archive && \
    mkdir -p /home/user/analysis

# /home/user/data/csvs/sales_central.csv
RUN cat >/home/user/data/csvs/sales_central.csv <<'EOF'
OrderID,Product,Quantity
1001,Widget,4
1002,Gadget,2
1003,Doodad,1
EOF

# /home/user/data/csvs/sales_east.csv
RUN cat >/home/user/data/csvs/sales_east.csv <<'EOF'
OrderID,Product,Quantity
2001,Thingamabob,5
2002,Widget,3
2003,Gadget,2
2004,Thingy,1
EOF

# /home/user/data/csvs/sales_west.csv
RUN cat >/home/user/data/csvs/sales_west.csv <<'EOF'
OrderID,Product,Quantity
3001,Gadget,2
3002,Widget,1
EOF

# /home/user/data/csvs/archive/sales_north.csv
RUN cat >/home/user/data/csvs/archive/sales_north.csv <<'EOF'
OrderID,Product,Quantity
4001,Doodad,3
4002,Thingamajig,4
4003,Gizmo,1
4004,Widget,2
4005,Gadget,3
EOF

# Set permissive permissions so the non-root runtime user can work
RUN chmod -R a+rX /home && \
    chmod -R a+rwX /home/user/analysis && \
    chmod 755 /home/user

LABEL Author="OpenAI ChatGPT"
LABEL Description="Environment for the quarterly sales CSV analysis task with pytest pre-installed."