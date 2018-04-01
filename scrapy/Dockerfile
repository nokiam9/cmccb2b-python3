FROM python:3.6
LABEL MAINTAINER="sj0225@icloud.com"

ARG AppMajorVersion
ARG AppMinorVersion

RUN pip install scrapy==1.5.0 \
    scrapyd==1.2.0 \
    scrapyd-client==1.1.0 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD scrapyd.conf /etc/scrapyd/scrapyd.conf

RUN mkdir /app
COPY ./app_${AppMajorVersion}_${AppMinorVersion} /app/

EXPOSE 6800
VOLUME /app/logs

WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["/usr/local/bin/scrapyd"]