FROM ubuntu:22.04

WORKDIR /langchain_ht

RUN apt-get update && apt-get -y install locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV STAGE_DIR=/tmp
RUN mkdir -p ${STAGE_DIR}

##############################################################################
# Installation/Basic Utilities
##############################################################################
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
        apt-get install -y --no-install-recommends \
        software-properties-common build-essential autotools-dev \
        build-essential python3 python3-pip git wget

COPY requirements.txt /langchain_ht/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY bundle /langchain_ht/bundle
COPY src /langchain_ht/src
COPY configs /langchain_ht/configs
COPY main.py /langchain_ht/main.py


CMD ["python3", "main.py"]