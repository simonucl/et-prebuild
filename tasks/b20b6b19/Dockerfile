# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: OpenAI-ChatGPT
# Description: Base image for headless local-HTML scraping task with test fixtures pre-installed.

LABEL Author="OpenAI-ChatGPT"
LABEL Description="Base image for headless local-HTML scraping task with test fixtures pre-installed."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl \
        wget \
        nano \
        git && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/website/pages && \
    mkdir -p /home/user/output && \
    chmod -R 0777 /home/user/output

RUN cat >/home/user/website/pages/page1.html <<'EOF'
<table id="weather">
<thead>
<tr><th>Date</th><th>Temperature</th><th>Humidity</th></tr>
</thead>
<tbody>
<tr><td>2021-06-01</td><td>25</td><td>60</td></tr>
<tr><td>2021-06-02</td><td>28</td><td>55</td></tr>
<tr><td>2021-06-03</td><td>27</td><td>50</td></tr>
<tr><td>2021-06-04</td><td>26</td><td>65</td></tr>
<tr><td>2021-06-05</td><td>30</td><td>45</td></tr>
</tbody>
</table>
EOF

RUN cat >/home/user/website/pages/page2.html <<'EOF'
<table id="weather">
<thead>
<tr><th>Date</th><th>Temperature</th><th>Humidity</th></tr>
</thead>
<tbody>
<tr><td>2021-06-04</td><td>26</td><td>65</td></tr>
<tr><td>2021-06-05</td><td>30</td><td>45</td></tr>
<tr><td>2021-06-06</td><td>31</td><td>40</td></tr>
<tr><td>2021-06-07</td><td>29</td><td>50</td></tr>
<tr><td>2021-06-08</td><td>28</td><td>55</td></tr>
</tbody>
</table>
EOF

RUN cat >/home/user/website/pages/page3.html <<'EOF'
<table id="weather">
<thead>
<tr><th>Date</th><th>Temperature</th><th>Humidity</th></tr>
</thead>
<tbody>
<tr><td>2021-06-09</td><td>26</td><td>60</td></tr>
<tr><td>2021-06-10</td><td>27</td><td>58</td></tr>
<tr><td>2021-06-11</td><td>30</td><td>48</td></tr>
<tr><td>2021-06-12</td><td>31</td><td>47</td></tr>
<tr><td>2021-06-13</td><td>29</td><td>50</td></tr>
</tbody>
</table>
EOF

RUN chmod -R 0755 /home/user/website

ENV PATH="/usr/bin:$PATH"

RUN chmod 755 /home/user

CMD echo "Container for the headless scraping task." && echo "Run your own commands inside the container to complete the assignment."