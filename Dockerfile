FROM python:3.6.5-stretch
RUN python3.6 -m pip install aiohttp
WORKDIR /root/code
