FROM alpine:latest

RUN apk add python3 py3-pip curl

RUN python3 -m pip install scapy pytest

COPY http_traffic_monitor/ /usr/local/bin/http_traffic_monitor