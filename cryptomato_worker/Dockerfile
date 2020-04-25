FROM ubuntu:18.04

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        bison \
        ca-certificates \
        flex \
        g++ \
        gcc \
        git \
        libprotobuf-dev \
        libprotobuf10 \
        libnl-route-3-dev \
        libnl-route-3-200 \
        make \
        pkg-config \
        protobuf-compiler \
    && git clone --depth=1 --branch=2.9 https://github.com/google/nsjail.git /nsjail \
    && cd /nsjail \
    && make \
    && mv /nsjail/nsjail /usr/sbin \
    && apt-get remove --purge -y \
        bison \
        ca-certificates \
        flex \
        g++ \
        gcc \
        git \
        libprotobuf-dev \
        libnl-route-3-dev \
        make \
        pkg-config \
        protobuf-compiler \
        $(apt-mark showauto) \
    && apt-get install -y --no-install-recommends \
        libprotobuf10 \
        libnl-route-3-200 \
        python3 python3-pip python3-setuptools gcc g++ python3-dev \
    && cd / \
    && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* ~/.cache/pip /nsjail

RUN pip3 install wheel
RUN pip3 install grpcio grpcio-tools

COPY . /cryptomato_worker

EXPOSE 10000

WORKDIR /
ENTRYPOINT ["/usr/bin/python3", "-u", "-m", "cryptomato_worker.worker"]
