FROM quay.io/redhat_emp1/3scale-demo-base:latest
LABEL maintainer="samander@redhat.com"

RUN mkdir -p /tmp/app
WORKDIR /tmp/app

ADD ./dist/*.tar.gz /tmp

CMD ["sh","-c", "python3 /tmp/app/wsgi.py"]