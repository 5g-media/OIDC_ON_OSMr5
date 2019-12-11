# This Dockerfile is intented for devops and deb package generation
#
# Use Dockerfile.local for running osm/NBI in a docker container from source
# Use Dockerfile.fromdeb for running osm/NBI in a docker container from last stable package


FROM ubuntu:16.04

RUN apt-get update && apt-get -y install git make libcurl4-gnutls-dev \
    libgnutls-dev debhelper apt-utils dh-make

