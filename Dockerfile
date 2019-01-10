FROM ubuntu:18.04
  
RUN apt-get update -yqq && apt-get -y -qq install \
    python3-setuptools \
    python3-dev \
    build-essential \
    python3-pip \
    pylint \
&& rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

RUN pip3 install pytest \
    pytest-cov \
    numpydoc
