FROM python:3.6
LABEL MAINTAINER="sj0225@icloud.com"

ARG AppMajorVersion
ARG AppMinorVersion

COPY ./requirements.txt /
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD scrapyd.conf /etc/scrapyd/scrapyd.conf

RUN mkdir /app
COPY ./app_${AppMajorVersion}_${AppMinorVersion} /app/

EXPOSE 6800
VOLUME /app/logs

ENTRYPOINT ["/usr/local/bin/scrapyd"]