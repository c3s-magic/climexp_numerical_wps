# vim:set ft=dockerfile:
FROM continuumio/miniconda3
MAINTAINER https://github.com/maartenplieger/climexp_numerical_wps
LABEL Description="Climate Explorer WPS service WPS" Vendor="Birdhouse" Version="0.1.0"

# Update Debian system
RUN apt-get update && apt-get install -y \
 build-essential \
&& rm -rf /var/lib/apt/lists/*

# Update conda
RUN conda update -n base conda

# Copy WPS project
COPY . /opt/wps

WORKDIR /opt/wps

# Create conda environment
RUN conda env create -n wps -f environment.yml
