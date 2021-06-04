from jenkins/agent:alpine

USER root
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 bash && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install pylint


