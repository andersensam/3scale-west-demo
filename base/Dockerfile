FROM registry.access.redhat.com/ubi8/ubi-minimal
LABEL maintainer="samander@redhat.com"

USER root
#RUN yum -y upgrade --disableplugin=subscription-manager nodejs npm gnutls nettle
RUN microdnf install python38

RUN mkdir -p /tmp/app
WORKDIR /tmp/app

ADD ./dist/*.tar.gz /tmp

RUN ["sh","-c", "pip3 install python-dateutil --upgrade"]
RUN ["sh","-c", "python3 /tmp/app/setup.py build"]
RUN ["sh","-c", "python3 /tmp/app/setup.py install"]

RUN chown -R 1001:1001 /tmp/app

USER 1001