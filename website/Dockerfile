FROM ubuntu:20.04

# Set the work directory 
WORKDIR /website

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
    flask  

COPY . .