FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
LABEL MAINTAINER="sj0225@icloud.com"

ARG AppMajorVersion
ARG AppMinorVersion

COPY ./app_${AppMajorVersion}_${AppMinorVersion} /app

WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY nginx/ssl/caogo.cn.crt /etc/nginx/ssl/caogo.cn.crt
COPY nginx/ssl/caogo.cn.key /etc/nginx/ssl/caogo.cn.key

COPY nginx/scrapyd_proxy.conf /etc/nginx/conf.d/
COPY nginx/ssl.conf /etc/nginx/conf.d/

