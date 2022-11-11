FROM ubuntu:20.04

# Set the work directory 
WORKDIR /physcov

# Minimal setup
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip

# Stop questions about geography
ARG DEBIAN_FRONTEND=noninteractive

# Install Python
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install \
    numpy \
    tqdm \
    prettytable \
    pandas \
    tabulate \
    ordered_set \
    scipy \
    shapely \
    matplotlib-venn

COPY . .