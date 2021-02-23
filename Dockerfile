FROM alpine:latest

RUN apk add python3 py3-pip curl

RUN python3 -m pip install scapy

COPY src/ /usr/local/bin/