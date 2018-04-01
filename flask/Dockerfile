FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
LABEL MAINTAINER="sj0225@icloud.com"

ARG AppMajorVersion
ARG AppMinorVersion

COPY ./app_${AppMajorVersion}_${AppMinorVersion} /app

WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
