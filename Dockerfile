FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN ./start.sh

CMD [ "python", "api.py" ]