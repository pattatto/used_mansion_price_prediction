FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
        sudo \
        wget \
        vim
WORKDIR /opt
RUN wget https://repo.continuum.io/archive/Anaconda3-2020.11-Linux-x86_64.sh && \
        sh /opt/Anaconda3-2020.11-Linux-x86_64.sh -b -p /opt/Anaconda3 && \
        rm -f Anaconda3-2020.11-Linux-x86_64.sh
ENV PATH /opt/Anaconda3/bin:$PATH
RUN pip install --upgrade pip
WORKDIR /
CMD ["/bin/bash"]